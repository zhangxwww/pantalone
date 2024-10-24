import datetime
import requests

from loguru import logger
from bs4 import BeautifulSoup
import akshare as ak
import pandas as pd

from libs.constant import CURRENCY_DICT


def get_china_bond_yield(date):
    url = f'https://yield.chinabond.com.cn/cbweb-mn/yc/searchYc?xyzSelect=txy&=&=&=&=&=&=&=&=&workTimes={date.strftime("%Y-%m-%d")}&dxbj=0&qxll=0,&yqqxN=N&yqqxK=K&ycDefIds=2c9081e50a2f9606010a3068cae70001,&wrjxCBFlag=0&locale=zh_CN'
    header = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://yield.chinabond.com.cn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://yield.chinabond.com.cn/',
        'Cookie': 'JSESSIONID=0000tv5-n87Xwvlq8VnkS8rS5Rc:-1; BIGipServerPool_srvnew_cbwebft_9080=!Fa2VX9jYVdqXMqizV2kA5FWxn4nt/mykDrlJlBwuLFn6b1ROAoXud+Soxpr53J1NXvpiKDNAHhIvS7I=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=0',
        'Content-Length': '0'
    }
    response = requests.post(url, headers=header)
    series = response.json()[0]['seriesData']
    y = list(filter(lambda x: x[0] == 1, series))[0][1]
    return y / 100


def get_lpr():
    res = requests.get('https://www.boc.cn/fimarkets/lilv/fd32/201310/t20131031_2591219.html')
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    lpr = []
    for tr in trs[1:]:
        tds = tr.find_all('td')
        date = tds[0].text
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        rate = tds[1].text[:-1]
        rate = float(rate) / 100
        lpr.append({'date': date, 'rate': rate})
    return lpr


def get_close(code, date):
    while True:
        date_str = date.strftime('%Y%m%d')
        df = ak.index_zh_a_hist(symbol=code, period='daily', start_date=date_str, end_date=date_str)
        if not df.empty:
            break
        logger.warning(f'Not found close data of {code} in {date}')
        date = date - datetime.timedelta(days=1)
    return df['收盘'][0]


def get_fund_name_from_symbol(symbol):
    return ak.fund_individual_basic_info_xq(symbol=symbol).loc[1, 'value']


def get_currency_rate(currency, start_date, end_date):
    df = ak.currency_boc_sina(symbol=currency, start_date=start_date, end_date=end_date)
    res = []
    for row in df.itertuples(index=False):
        res.append({
            'date': row.日期,
            'rate': round(row.中行汇买价 / 100, 4)
        })
    return res


def get_latest_net_value_of_fund(symbol):
    return ak.fund_open_fund_info_em(symbol=symbol, indicator="单位净值走势")['单位净值'].iloc[-1]


def get_fund_holding(symbol, year, type_):

    func = {
        'stock': ak.fund_portfolio_hold_em,
        'bond': ak.fund_portfolio_bond_hold_em
    }
    try:
        df = func[type_](symbol=symbol, date=year)

        df['基金代码'] = symbol
        df['年份'] = year
        df['季度'] = df['季度'].apply(lambda x: x.split('年')[1].split('季度')[0])
        cn_type = '股票' if type_ == 'stock' else '债券'
        df = df[['年份', '季度', '基金代码', f'{cn_type}代码', f'{cn_type}名称', '占净值比例']]
        res = []
        for row in df.itertuples(index=False):
            res.append({
                'year': row.年份,
                'quarter': int(row.季度),
                'fund_code': row.基金代码,
                'code': row[3],
                'name': row[4],
                'ratio': row.占净值比例,
                'type': type_
            })
    except:
        res = []
    return res


def _clip_date(df, start, end):
    df = df[(df['date'] >= datetime.datetime.strptime(start, '%Y%m%d').date())
            & (df['date'] <= datetime.datetime.strptime(end, '%Y%m%d').date())]
    return df

def _resample(daily_kline_df, period):
    df = daily_kline_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    sample = 'W' if period == 'weekly' else 'M'
    agg_df = df.resample(sample).agg({
        'open': 'first',
        'close': 'last',
        'high': 'max',
        'low': 'min',
        'volume': 'sum'
    }).dropna()
    agg_df = agg_df.reset_index()
    return agg_df


def get_kline(code, start_date, end_date, period='daily', market='index-CN'):
    need_clip = False
    need_resample = False

    if market == 'index-CN':
        df = ak.index_zh_a_hist(symbol=code, period=period, start_date=start_date, end_date=end_date)
        df = df.rename(columns={'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交额': 'volume'})

    elif market == 'index-HK':
        df = ak.stock_hk_index_daily_sina(symbol=code)
        need_clip = need_resample = True

    elif market == 'index-US':
        df = ak.index_us_stock_sina(symbol=code)
        need_clip = need_resample = True

    elif market == 'index-qvix':
        if code == '300ETF':
            df = ak.index_option_300etf_qvix()
        elif code == '50ETF':
            df = ak.index_option_50etf_qvix()
        df['volume'] = 0
        need_clip = need_resample = True

    elif market == 'future-zh':
        df = ak.futures_zh_daily_sina(symbol=code)
        df['date'] = pd.to_datetime(df['date']).dt.date
        need_clip = need_resample = True

    else:
        raise NotImplementedError

    if need_clip:
        df = _clip_date(df, start_date, end_date)
    if need_resample:
        if period != 'daily':
            df = _resample(df, period)

    res = []
    for row in df.itertuples(index=False):
        res.append({
            'date': row.date,
            'open': row.open,
            'close': row.close,
            'high': row.high,
            'low': row.low,
            'volume': row.volume
        })
    return res


def get_market_data(instrument, start_date, end_date):
    need_clip = False
    logger.debug(f'Get market data of {instrument} from {start_date} to {end_date}')

    if instrument == 'LPR':
        df = ak.macro_china_lpr()
        df = df.rename(columns={'TRADE_DATE': 'date'})
        extract_columns = {
            'LPR1Y': 'lpr_1y',
            'LPR5Y': 'lpr_5y',
            'RATE_1': 'short_term_rate',
            'RATE_2': 'mid_term_rate',
        }
        need_clip = True
    elif instrument in CURRENCY_DICT:
        currency = CURRENCY_DICT[instrument]
        df = ak.currency_boc_sina(symbol=currency, start_date=start_date, end_date=end_date)
        df = df.rename(columns={'日期': 'date', '中行汇买价': 'rate'})
        df['rate'] = df['rate'] / 100
        extract_columns = {
            'rate': currency
        }
    elif instrument == 'leverage-CN':
        df = ak.macro_cnbs()
        df['date'] = df['年份'].apply(lambda x: f'{x}-01')
        df['date'] = pd.to_datetime(df['date']).dt.date
        extract_columns = {
            '居民部门': 'leverage_resident',
            '非金融企业部门': 'leverage_non_financial',
            '政府部门': 'leverage_government',
            '中央政府': 'leverage_central_government',
            '地方政府': 'leverage_local_government',
            '实体经济部门': 'leverage_real_economy',
            '金融部门资产方': 'leverage_financial_assets',
            '金融部门负债方': 'leverage_financial_liabilities',
        }
        need_clip = True
    else:
        raise NotImplementedError

    if need_clip:
        df = _clip_date(df, start_date, end_date)

    res = []
    for row in df.itertuples(index=False):
        r = {'date': row.date}
        for k, v in extract_columns.items():
            r[v] = getattr(row, k)
        res.append(r)

    return res



if __name__ == '__main__':
    print(get_market_data('leverage-CN', '20210101', '20220110'))