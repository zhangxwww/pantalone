import json
import base64
from datetime import datetime
from joblib import Parallel, delayed
import itertools

from loguru import logger

import spider
import sql_app.schemas as schemas
import sql_app.crud as crud
from utils import trans_str_date_to_trade_date, get_one_quarter_before


INDEX_CODES = [
    '000001',  # 上证指数
    '000012',  # 国债指数
]


def get_china_bond_yield_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = crud.get_CN1YR_data(db, query_dates)

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
    crud.create_CN1YR_data_from_list(db, not_found_dates_yield)

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


def get_lpr_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = crud.get_lpr_data(db, query_dates)
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

        crud.create_lpr_data_from_list(db, add_to_db_data)

        data = aligned
    else:
        data = db_data_list

    return data


def get_index_close_data(db, dates):
    query_dates = [trans_str_date_to_trade_date(d) for d in dates]

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = crud.get_index_close_data(db, query_dates)
    db_data_list = [{'date': d.date, 'close': d.close, 'code': d.code} for d in db_data]

    logger.debug('DB data: ')
    logger.debug(db_data_list)

    required_data = set(itertools.product(INDEX_CODES, query_dates))

    not_found_data = list(required_data - set((d.code, d.date) for d in db_data))

    logger.debug('Not found data: ')
    logger.debug(not_found_data)

    def _f(code, date):
        close = spider.get_close(code, date)
        return schemas.IndexCloseDataCreate(date=date, close=close, code=code)

    not_found_dates_close = Parallel(n_jobs=-1)(delayed(_f)(code, date) for code, date in not_found_data)

    crud.create_index_close_data_from_list(db, not_found_dates_close)

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


def get_fund_name(db, symbol):
    db_data = crud.get_fund_name(db, symbol)
    if db_data is not None:
        logger.debug(f'Get fund name from db: {db_data.name}')
        return db_data.name
    else:
        name = spider.get_fund_name_from_symbol(symbol)
        item = schemas.FundNameDataCreate(symbol=symbol, name=name)
        crud.create_fund_name(db, item)
        logger.debug(f'Get fund name from spider: {name}')
        return name


def save_base64_data(db, data):
    content = base64.b64decode(data)
    json_data = json.loads(content.decode('utf-8'))
    crud.create_table_from_json(db, json_data)


def _get_cash_data_from_db(db):
    cash_data = []
    all_data = crud.get_all_cash_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_cash_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'amount': his.amount,
                'beginningTime': his.beginningTime
            }
            history_list.append(h)
        cash_data.append({
            'id': history_id,
            'history': history_list
        })
    return cash_data

def _get_monetary_fund_data_from_db(db):
    monetary_data = []
    all_data = crud.get_all_monetary_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_monetary_fund_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'beginningAmount': his.beginningAmount,
                'beginningTime': his.beginningTime,
                'beginningShares': his.beginningShares,
                'currentAmount': his.currentAmount,
                'currentTime': his.currentTime,
                'currentShares': his.currentShares,
                'fastRedemption': his.fastRedemption,
                'holding': his.holding
            }
            history_list.append(h)
        monetary_data.append({
            'id': history_id,
            'history': history_list
        })
    return monetary_data

def _get_fixed_deposit_data_from_db(db):
    fixed_deposit_data = []
    all_data = crud.get_all_fixed_deposit_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_fixed_deposit_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'beginningAmount': his.beginningAmount,
                'beginningTime': his.beginningTime,
                'rate': his.rate,
                'maturity': his.maturity
            }
            history_list.append(h)
        fixed_deposit_data.append({
            'id': history_id,
            'history': history_list
        })
    return fixed_deposit_data

def _get_fund_data_from_db(db):
    fund_data = []
    all_data = crud.get_all_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_fund_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'symbol': his.symbol,
                'currentNetValue': his.currentNetValue,
                'currentShares': his.currentShares,
                'currentTime': his.currentTime,
                'holding': his.holding,
                'lockupPeriod': his.lockupPeriod
            }
            history_list.append(h)
        fund_data.append({
            'id': history_id,
            'history': history_list
        })
    return fund_data


def get_data_from_db(db):
    return {
        'cashData': _get_cash_data_from_db(db),
        'monetaryFundData': _get_monetary_fund_data_from_db(db),
        'fixedDepositData': _get_fixed_deposit_data_from_db(db),
        'fundData': _get_fund_data_from_db(db)
    }


def add_cash_history(db, data):
    item = schemas.CashDataHistoryItemCreate(**data.content.model_dump(), beginningTime=datetime.now().date())
    crud.create_cash_data_history_item(db, item, data.id)


def add_monetary_fund_history(db, data):
    content = data.content.model_dump()

    logger.debug(content)

    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    content['currentTime'] = datetime.now().date()
    content['beginningShares'] = content['beginningAmount']
    item = schemas.MonetaryFundDataHistoryItemCreate(**content)
    crud.create_monetary_fund_data_history_item(db, item, data.id)


def add_fixed_deposit_history(db, data):
    content = data.content.model_dump()
    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    item = schemas.FixedDepositDataHistoryItemCreate(**content)
    crud.create_fixed_deposit_data_history_item(db, item, data.id)


def add_fund_history(db, data):
    content = data.content.model_dump()
    content['currentTime'] = datetime.now().date()
    item = schemas.FundDataHistoryItemCreate(**content)
    crud.create_fund_data_history_item(db, item, data.id)


def get_refreshed_fund_net_value(symbols):
    def _f(symbol):
        net_value = spider.get_latest_net_value_of_fund(symbol)
        return {'symbol': symbol, 'value': net_value}

    ret = Parallel(n_jobs=-1)(delayed(_f)(symbol) for symbol in symbols)
    return ret


def get_fund_holding_data(db, symbols):

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_quarter = (current_month - 1) // 3 + 1

    logger.debug(f'Current: {current_year}Q{current_quarter}')

    def _search_in_db(symbols, year, quarter, holdings, found, type_):
        for symbol in symbols:
            holding = crud.get_fund_holding_data(db, year, quarter, symbol, type_)
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

    def _search_by_spider(symbols, year, quarter, holdings, found, type_):
        spider_res = Parallel(n_jobs=-1)(delayed(_f)(symbol, year, quarter, type_) for symbol in symbols)

        for symbol, quarter_holding, all_holding in spider_res:

            if quarter_holding:
                holdings[symbol] = quarter_holding
                found.add(symbol)

            for h in all_holding:
                item = schemas.FundHoldingDataCreate(**h)
                crud.create_fund_holding_data_if_not_exist(db, item)

        logger.debug(f'Spider result ({year}Q{quarter}): {holdings.keys()}')

    year, quarter = current_year, current_quarter

    spider_year = None

    stock_found = set()
    bond_found = set()
    stock_holdings = {}
    bond_holdings = {}

    for _ in range(16):
        year, quarter = get_one_quarter_before(year, quarter)

        not_found_stock_symbols = set(symbols) - stock_found
        not_found_bond_symbols = set(symbols) - bond_found

        logger.debug(f'Not found stock symbols before db ({year}Q{quarter}): {not_found_stock_symbols}')
        logger.debug(f'Not found bond symbols before db ({year}Q{quarter}): {not_found_bond_symbols}')

        if len(not_found_stock_symbols) == 0 and len(not_found_bond_symbols) == 0:
            break

        _search_in_db(not_found_stock_symbols, year, quarter, stock_holdings, stock_found, 'stock')
        _search_in_db(not_found_bond_symbols, year, quarter, bond_holdings, bond_found, 'bond')

        logger.debug(f'Already found stock in db ({year}Q{quarter}): {stock_found}')
        logger.debug(f'Already found bond in db ({year}Q{quarter}): {bond_found}')

        if spider_year == year:
            continue

        spider_year = year

        not_found_stock_symbols = set(symbols) - stock_found
        not_found_bond_symbols = set(symbols) - bond_found

        logger.debug(f'Not found stock symbols before spider ({year}Q{quarter}): {not_found_stock_symbols}')
        logger.debug(f'Not found bond symbols before spider ({year}Q{quarter}): {not_found_bond_symbols}')

        if len(not_found_stock_symbols) == 0 and len(not_found_bond_symbols) == 0:
            break

        _search_by_spider(not_found_stock_symbols, year, quarter, stock_holdings, stock_found, 'stock')
        _search_by_spider(not_found_bond_symbols, year, quarter, bond_holdings, bond_found, 'bond')

        logger.debug(f'Already found stock in spider ({year}Q{quarter}): {stock_found}')
        logger.debug(f'Already found bond in spider ({year}Q{quarter}): {bond_found}')

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