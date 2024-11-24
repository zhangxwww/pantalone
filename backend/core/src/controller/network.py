import math

from datetime import datetime, timedelta
from joblib import Parallel, delayed
import itertools

from loguru import logger

import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import pairwise_distances

import libs.spider as spider
import sql_app.schemas as schemas
import sql_app.crud as crud
from libs.indicator import list_dict_to_dataframe, dataframe_to_list_dict, boll
from libs.decorators.cache import CacheWithExpiration
from libs.utils.date_transform import trans_str_date_to_trade_date, get_one_quarter_before, trans_date_to_trade_date
from libs.constant import INDEX_CODES, CURRENCY_DICT, INSTRUMENT_CODES, KLINE_START


cache = CacheWithExpiration()

async def get_china_bond_yield_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = await crud.get_CN1YR_data(db, query_dates)

    db_data_list = [{'date': d.date, 'yield': d.yield_1yr} for d in db_data]

    logger.debug('DB data: ')
    logger.debug(db_data_list)

    not_found_dates = list(set(query_dates) - set(d.date for d in db_data))

    logger.debug('Not found dates: ')
    logger.debug(not_found_dates)

    not_found_dates_yield = []
    for date in not_found_dates:
        yield_1yr = spider.get_china_bond_yield(date)
        item = schemas.CN1YRDataCreate(date=date, yield_1yr=yield_1yr)
        not_found_dates_yield.append(item)
    await crud.create_CN1YR_data_from_list(db, not_found_dates_yield)

    spider_data = [{'date': d.date, 'yield': d.yield_1yr} for d in not_found_dates_yield]

    logger.debug('Spider data: ')
    logger.debug(spider_data)

    data = db_data_list + spider_data
    data = sorted(data, key=lambda x: x['date'])

    logger.debug('Final data: ')
    logger.debug(data)

    return data

def _align_lpr_date(lpr_list, query_dates):
    lpr_list = sorted(lpr_list, key=lambda x: x['date'])
    query_dates = sorted(query_dates)

    logger.debug('LPR list: ')
    logger.debug(lpr_list)

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    res = []
    lpr_index = 0
    for qd in query_dates:
        if lpr_index >= len(lpr_list):
            break
        l = float('nan')
        while True:
            lpr = lpr_list[lpr_index]
            lpr_date = lpr['date']
            if qd >= lpr_date:
                l = lpr['rate']
                lpr_index += 1
                if lpr_index >= len(lpr_list):
                    break
            else:
                break
        res.append({'date': qd, 'rate': l})
    return res

async def get_lpr_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = await crud.get_lpr_data(db, query_dates)
    db_data_list = [{'date': d.date, 'rate': d.lpr} for d in db_data]

    logger.debug('DB data: ')
    logger.debug(db_data_list)

    not_found_dates = list(set(query_dates) - set(d.date for d in db_data))

    logger.debug('Not found dates: ')
    logger.debug(not_found_dates)

    if len(not_found_dates) > 0:

        spider_data = spider.get_lpr()

        logger.debug('Spider data:')
        logger.debug(spider_data)

        aligned = _align_lpr_date(spider_data, query_dates)

        logger.debug('Aligned data:')
        logger.debug(aligned)

        add_to_db_data = [schemas.LPRDataCreate(date=d['date'], lpr=d['rate'])
                          for d in aligned if d['date'] in not_found_dates]

        logger.debug('Add to db: ')
        logger.debug(add_to_db_data)

        await crud.create_lpr_data_from_list(db, add_to_db_data)

        data = aligned
    else:
        data = db_data_list

    return data

async def get_index_close_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = await crud.get_index_close_data(db, query_dates)
    db_data_list = [{'date': d.date, 'close': d.close, 'code': d.code} for d in db_data]

    required_data = set(itertools.product(INDEX_CODES, query_dates))

    not_found_data = list(required_data - set((d.code, d.date) for d in db_data))

    def _f(code, date):
        close = spider.get_close(code, date)
        return schemas.IndexCloseDataCreate(date=date, close=close, code=code)

    not_found_dates_close = Parallel(n_jobs=-1)(delayed(_f)(code, date) for code, date in not_found_data)

    await crud.create_index_close_data_from_list(db, not_found_dates_close)

    spider_data = [{'date': d.date, 'close': d.close, 'code': d.code} for d in not_found_dates_close]

    logger.debug('Spider data: ')
    logger.debug(spider_data)

    data = db_data_list + spider_data
    data = sorted(data, key=lambda x: x['date'])

    logger.debug('All data: ')
    logger.debug(data)

    final_data = []
    for date, group in itertools.groupby(data, key=lambda x: x['date']):
        d = {'date': date}
        for item in group:
            d[item['code']] = item['close']
        final_data.append(d)

    logger.debug('Final data: ')
    logger.debug(final_data)

    return final_data

async def get_latest_currency_rate(db, symbol):
    if symbol == 'CNY':
        return 1.0
    date = datetime.now().date()
    working_date_str = trans_date_to_trade_date(date).strftime('%Y%m%d')
    current_date_str = date.strftime('%Y%m%d')
    logger.debug(working_date_str)

    res = spider.get_currency_rate(CURRENCY_DICT[symbol], start_date=working_date_str, end_date=current_date_str)
    logger.debug(res)

    return res[-1]['rate']

@cache(expiration_time=3600 * 24 * 7)
async def get_fund_name(db, symbol):
    db_data = await crud.get_fund_name(db, symbol)
    if db_data is not None:
        logger.debug(f'Get fund name from db: {db_data.name}')
        return db_data.name
    else:
        try:
            name = spider.get_fund_name_from_symbol(symbol)
        except KeyError:
            logger.warning(f'Cannot find fund name for symbol: {symbol}')
            return None
        item = schemas.FundNameDataCreate(symbol=symbol, name=name)
        await crud.create_fund_name(db, item)
        logger.debug(f'Get fund name from spider: {name}')
        return name

async def get_refreshed_fund_net_value(symbols):
    def _f(symbol):
        net_value = spider.get_latest_net_value_of_fund(symbol)
        return {'symbol': symbol, 'value': net_value}

    ret = Parallel(n_jobs=-1)(delayed(_f)(symbol) for symbol in symbols)
    return ret

@cache(expiration_time=3600 * 24 * 7)
async def get_fund_holding_data(db, symbols):

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_quarter = (current_month - 1) // 3 + 1

    logger.debug(f'Current: {current_year}Q{current_quarter}')

    async def _search_in_db(symbols, year, quarter, holdings, found, type_):
        for symbol in symbols:
            holding = await crud.get_fund_holding_data(db, year, quarter, symbol, type_)
            if holding:
                holdings[symbol] = [{
                    'fund_code': h.fund_code,
                    'code': h.code,
                    'name': h.name,
                    'ratio': h.ratio,
                    'type': h.type,
                    'year': h.year,
                    'quarter': h.quarter
                } for h in holding]
                found.add(symbol)

        logger.debug(f'Found in db ({year}Q{quarter}): {holdings.keys()}')

    def _f(symbol, year, quarter, type_):
        holding = spider.get_fund_holding(symbol, year, type_)
        ret_holding = [h for h in holding if h['quarter'] == quarter]
        return symbol, ret_holding, holding


    async def _skip_not_found_in_spider_symbols(symbols, year, quarter):
        res = set()
        for s in symbols:
            if not await crud.find_holding_not_found_in_spider_history_data(db, s, year, quarter):
                res.add(s)
            else:
                logger.debug(f'Skip {s} in {year}Q{quarter}')
        return res


    async def _search_by_spider(symbols, year, quarter, holdings, found, type_):
        symbols = await _skip_not_found_in_spider_symbols(symbols, year, quarter)
        spider_res = Parallel(n_jobs=-1)(delayed(_f)(symbol, year, quarter, type_) for symbol in symbols)

        for symbol, quarter_holding, all_holding in spider_res:

            if quarter_holding:
                holdings[symbol] = quarter_holding
                found.add(symbol)
            elif year != current_year or quarter != current_quarter:
                item = schemas.HoldingNotFoundInSpiderHistoryCreate(code=symbol, year=year, quarter=quarter)
                await crud.create_holding_not_found_in_spider_history_data(db, item)

                logger.debug(f'Add {symbol} in {year}Q{quarter} to not found in spider history')

            for h in all_holding:
                item = schemas.FundHoldingDataCreate(**h)
                await crud.create_fund_holding_data_if_not_exist(db, item)

        logger.debug(f'Spider result ({year}Q{quarter}): {holdings.keys()}')

    year, quarter = current_year, current_quarter

    spider_year = None

    stock_found = set()
    bond_found = set()
    stock_holdings = {}
    bond_holdings = {}

    not_found_stock_symbols = set(symbols[:])
    not_found_bond_symbols = set(symbols[:])

    for _ in range(12):

        not_found_stock_symbols = not_found_stock_symbols - stock_found
        not_found_bond_symbols = not_found_bond_symbols - bond_found

        logger.debug(f'Not found stock symbols before db ({year}Q{quarter}): {not_found_stock_symbols}')
        logger.debug(f'Not found bond symbols before db ({year}Q{quarter}): {not_found_bond_symbols}')

        if len(not_found_stock_symbols) == 0 and len(not_found_bond_symbols) == 0:
            break

        await _search_in_db(not_found_stock_symbols, year, quarter, stock_holdings, stock_found, 'stock')
        await _search_in_db(not_found_bond_symbols, year, quarter, bond_holdings, bond_found, 'bond')

        logger.debug(f'Already found stock in db ({year}Q{quarter}): {stock_found}')
        logger.debug(f'Already found bond in db ({year}Q{quarter}): {bond_found}')

        if spider_year != year:
            spider_year = year

            not_found_stock_symbols = not_found_stock_symbols - stock_found
            not_found_bond_symbols = not_found_bond_symbols - bond_found

            logger.debug(f'Not found stock symbols before spider ({year}Q{quarter}): {not_found_stock_symbols}')
            logger.debug(f'Not found bond symbols before spider ({year}Q{quarter}): {not_found_bond_symbols}')

            if len(not_found_stock_symbols) == 0 and len(not_found_bond_symbols) == 0:
                break

            await _search_by_spider(not_found_stock_symbols, year, quarter, stock_holdings, stock_found, 'stock')
            await _search_by_spider(not_found_bond_symbols, year, quarter, bond_holdings, bond_found, 'bond')

            logger.debug(f'Already found stock in spider ({year}Q{quarter}): {stock_found}')
            logger.debug(f'Already found bond in spider ({year}Q{quarter}): {bond_found}')

        year, quarter = get_one_quarter_before(year, quarter)

    not_found_stock_symbols = set(symbols) - stock_found
    not_found_bond_symbols = set(symbols) - bond_found

    for symbol in not_found_stock_symbols:
        stock_holdings[symbol] = []

    for symbol in not_found_bond_symbols:
        bond_holdings[symbol] = []

    holdings = {}
    for symbol in symbols:
        holdings[symbol] = {
            'stock': stock_holdings[symbol],
            'bond': bond_holdings[symbol]
        }

    return holdings

async def get_fund_holding_relevance_data(fund_holding_data):
    def _to_one_hot(data):

        all_data = set(item for sublist in data for item in sublist)
        all_data = [(s, ) for s in all_data]

        logger.debug(f'All data: {len(all_data)}')

        encoder = MultiLabelBinarizer()
        encoder.fit(all_data)

        ret = []
        for d in data:
            if len(d) == 0:
                ret.append(np.zeros((1, len(all_data))))
                continue

            d = [tuple(d)]
            one_hot = encoder.transform(d)

            logger.debug(f'One hot: {one_hot.shape}')

            ret.append(one_hot)
        return np.concatenate(ret, axis=0)

    stock_data = [[i['code'] for i in item['stock']] for item in fund_holding_data.values()]
    bond_data = [[i['code'] for i in item['bond']] for item in fund_holding_data.values()]

    stock_one_hot = _to_one_hot(stock_data)
    bond_one_hot = _to_one_hot(bond_data)

    logger.debug(f'Stock one hot: {stock_one_hot.shape}')
    logger.debug(f'Bond one hot: {bond_one_hot.shape}')

    all_one_hot = np.concatenate((stock_one_hot, bond_one_hot), axis=1)

    logger.debug(f'All one hot: {all_one_hot.shape}')

    def _pairwise_relevance(data):
        try:
            return pairwise_distances(data, metric='euclidean')
        except ValueError:
            return np.zeros((data.shape[0], data.shape[0]))

    stock_relevance = _pairwise_relevance(stock_one_hot).tolist()
    bond_relevance = _pairwise_relevance(bond_one_hot).tolist()
    all_relevance = _pairwise_relevance(all_one_hot).tolist()

    def _decomposition(data):
        try:
            perplexity = min(30, data.shape[0] - 1)
            tsne = TSNE(n_components=2, perplexity=perplexity)
            scaler = MinMaxScaler()
            pos = tsne.fit_transform(data)
            pos = scaler.fit_transform(pos)
            return pos
        except ValueError:
            return np.zeros((data.shape[0], 2))

    stock_pos = _decomposition(stock_one_hot).tolist()
    bond_pos = _decomposition(bond_one_hot).tolist()
    all_pos = _decomposition(all_one_hot).tolist()

    return {
        'stock': stock_relevance,
        'bond': bond_relevance,
        'all': all_relevance,
        'stockPos': stock_pos,
        'bondPos': bond_pos,
        'allPos': all_pos,
        'order': list(fund_holding_data.keys())
    }

@cache(expiration_time=3600)
async def get_kline_data(db, query):
    code = query.code
    period = query.period
    market = query.market

    data_in_db = await crud.get_kline_data(db, code, period, market)
    res = [{
        'date': data.date,
        'open': data.open,
        'close': data.close,
        'high': data.high,
        'low': data.low,
        'volume': data.volume
    } for data in data_in_db]

    logger.debug(f'Found {len(res)} data in db')

    if len(res) > 0:
        last_date_in_db = res[-1]['date']
        next_day_of_last_date = last_date_in_db + timedelta(days=1)
        spider_start_date = next_day_of_last_date
    else:
        spider_start_date = KLINE_START[period]
    spider_end_date = datetime.now().date()
    spider_end_date = trans_date_to_trade_date(spider_end_date)

    if spider_start_date <= spider_end_date:

        spider_start_date = spider_start_date.strftime('%Y%m%d')
        spider_end_date = spider_end_date.strftime('%Y%m%d')

        logger.debug(f'Spider start date: {spider_start_date}')
        logger.debug(f'Spider end date: {spider_end_date}')

        data_from_spider = spider.get_kline(code, spider_start_date, spider_end_date, period, market)
        await crud.create_kline_data_from_list(db, data_from_spider, code, period, market)

        logger.debug(f'Found {len(data_from_spider)} data in spider')

        res.extend(data_from_spider)

    df = list_dict_to_dataframe(res)
    df = boll(df, window=20, width=2)
    df.fillna(0, inplace=True)
    res = dataframe_to_list_dict(df)

    return res

@cache(expiration_time=3600)
async def get_market_data(db, instrument):
    codes = INSTRUMENT_CODES[instrument]

    res = {}
    for code in codes:
        data_in_db = await crud.get_market_data(db, code)
        res[code] = [{
            'date': data.date,
            'price': data.price,
        } for data in data_in_db]

    logger.debug(f'Found {len(res[codes[0]])} data in db')

    if len(res[codes[0]]) > 0:
        last_date_in_db = res[codes[0]][-1]['date']
        next_day_of_last_date = last_date_in_db + timedelta(days=1)
        spider_start_date = next_day_of_last_date
    else:
        spider_start_date = KLINE_START['daily']
    spider_end_date = datetime.now().date()
    spider_end_date = trans_date_to_trade_date(spider_end_date)

    if spider_start_date <= spider_end_date:
        spider_start_date = spider_start_date.strftime('%Y%m%d')
        spider_end_date = spider_end_date.strftime('%Y%m%d')

        logger.debug(f'Spider start date: {spider_start_date}')
        logger.debug(f'Spider end date: {spider_end_date}')

        data_from_spider = spider.get_market_data(instrument, spider_start_date, spider_end_date)

        for code in codes:
            data = [{
                'date': d['date'],
                'price': d[code],
            } for d in data_from_spider]
            await crud.create_market_data_from_list(db, data, code)

            res[code].extend(data)

        logger.debug(f'Found {len(data_from_spider)} data in spider')

    for code in codes:
        r_code = res[code]
        for r in r_code:
            if r['price'] is not None and math.isnan(r['price']):
                r['price'] = None

    return res

@cache(expiration_time=3600 * 24 * 7)
async def get_stock_bond_info(db, stocks, bonds):
    stock_info = []
    stock_found = set()
    for stock in stocks:
        data = await crud.get_stock_info_data(db, stock)
        if data:
            stock_info.append({
                'code': data.code,
                'abbreviation': data.abbreviation,
                'name': data.name,
                'industry': data.industry,
                'market': data.market
            })
            stock_found.add(stock)

    bond_info = []
    bond_found = set()
    for bond in bonds:
        data = await crud.get_bond_info_data(db, bond)
        if data:
            bond_info.append({
                'code': data.code,
                'abbreviation': data.abbreviation,
                'name': data.name,
                'type': data.type,
                'level': data.level
            })
            bond_found.add(bond)

    def _crawl_stock(stock):
        try:
            data = spider.get_stock_info(stock)
        except TypeError:
            return stock, None
        return stock, {
            'code': stock,
            'abbreviation': data['股票简称'] or '',
            'name': data['公司名称'] or '',
            'industry': data['所属行业'] or '',
            'market': data['所在市场'] or ''
        }

    def _crawl_bond(bond):
        try:
            data = spider.get_bond_info(bond)
        except (TypeError, NotImplementedError):
            return bond, None
        return bond, {
            'code': bond,
            'abbreviation': data['债券简称'] or '',
            'name': data['债券名称'] or '',
            'type': data['债券类型'] or '',
            'level': data['信用等级'] or ''
        }

    stock_not_found = set(stocks) - stock_found
    bond_not_found = set(bonds) - bond_found

    spider_stock_info = Parallel(n_jobs=-1)(delayed(_crawl_stock)(stock) for stock in stock_not_found)
    spider_bond_info = Parallel(n_jobs=-1)(delayed(_crawl_bond)(bond) for bond in bond_not_found)

    for code, s in spider_stock_info:
        if s:
            stock_info.append(s)
        else:
            logger.warning(f'Not found stock: {code}')
    for code, b in spider_bond_info:
        if b:
            bond_info.append(b)
        else:
            logger.warning(f'Not found bond: {code}')

    await crud.create_stock_info_data_from_list(db, stock_info)
    await crud.create_bond_info_data_from_list(db, bond_info)

    return {
        'stock': stock_info,
        'bond': bond_info
    }
