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
    elif instrument == 'unemployment-rate-CN':
        df = ak.macro_china_urban_unemployment()
        df['date'] = df['date'].apply(lambda x: f'{x[:4]}-{x[4:6]}-01')
        df['date'] = pd.to_datetime(df['date']).dt.date
        replace = {
            '31个大城市城镇调查失业率': '三十一个大城市城镇调查失业率',
            '全国城镇16—24岁劳动力失业率': '全国城镇十六至二十四岁劳动力失业率',
            '全国城镇25—59岁劳动力失业率': '全国城镇二十五至五十九岁劳动力失业率',
            '全国城镇不包含在校生的16—24岁劳动力失业率': '全国城镇不包含在校生的十六至二十四岁劳动力失业率',
            '全国城镇不包含在校生的25—29岁劳动力失业率': '全国城镇不包含在校生的二十五至二十九岁劳动力失业率',
            '全国城镇不包含在校生的30—59岁劳动力失业率': '全国城镇不包含在校生的三十至五十九岁劳动力失业率',
        }
        extract_columns = {
            '全国城镇调查失业率': 'national_urban_unemployment_rate',
            '三十一个大城市城镇调查失业率': '31_major_cities_urban_unemployment_rate',
            '全国城镇本地户籍劳动力失业率': 'national_urban_local_unemployment_rate',
            '全国城镇外来户籍劳动力失业率': 'national_urban_migrant_unemployment_rate',
            '全国城镇十六至二十四岁劳动力失业率': '16_24_urban_unemployment_rate',
            '全国城镇二十五至五十九岁劳动力失业率': '25_59_urban_unemployment_rate',
            '全国城镇不包含在校生的十六至二十四岁劳动力失业率': '16_24_urban_unemployment_rate_excluding_students',
            '全国城镇不包含在校生的二十五至二十九岁劳动力失业率': '25_29_urban_unemployment_rate_excludng_students',
            '全国城镇不包含在校生的三十至五十九岁劳动力失业率': '30_59_urban_unemployment_rate_excludng_students',
        }
        dfs = []
        for col in df['item'].unique():
            df_col = df[df['item'] == col].copy()
            col = replace[col] if col in replace else col
            df_col[col] = df_col['value']
            df_col = df_col[['date', col]]
            dfs.append(df_col)
        merged = dfs[0]
        for df in dfs[1:]:
            merged = pd.merge(merged, df, on='date', how='outer')
        df = merged.sort_values('date')
        need_clip = True
    elif instrument == 'AFRE-CN':
        df = ak.macro_china_shrzgm()
        df['date'] = df['月份'].apply(lambda x: f'{x[:4]}-{x[4:6]}-01')
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df.rename(columns={
            '其中-人民币贷款': '人民币贷款',
            '其中-委托贷款外币贷款': '委托贷款外币贷款',
            '其中-委托贷款': '委托贷款',
            '其中-信托贷款': '信托贷款',
            '其中-未贴现银行承兑汇票': '未贴现银行承兑汇票',
            '其中-企业债券': '企业债券',
            '其中-非金融企业境内股票融资': '非金融企业境内股票融资',
        })
        extract_columns = {
            '社会融资规模增量': 'aggregate_financing_to_the_real_economy',
            '人民币贷款': 'renminbi_loan',
            '委托贷款外币贷款': 'entrusted_foreign_currency_loan',
            '委托贷款': 'entrusted_loan',
            '信托贷款': 'trust_loan',
            '未贴现银行承兑汇票': 'undiscounted_bank_acceptance_bill',
            '企业债券': 'corporate_bonds',
            '非金融企业境内股票融资': 'domestic_stock_financing_for_non_financial_enterprises',
        }
        need_clip = True
    elif instrument == 'GDP-CN':
        df = ak.macro_china_gdp_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'gdp_cn_current',
            '预测值': 'gdp_cn_predict',
            '前值': 'gdp_cn_previous'
        }
        need_clip = True
    elif instrument == 'CPI-yearly-CN':
        df = ak.macro_china_cpi_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'cpi_yearly_cn_current',
            '预测值': 'cpi_yearly_cn_predict',
            '前值': 'cpi_yearly_cn_previous'
        }
        need_clip = True
    elif instrument == 'CPI-monthly-CN':
        df = ak.macro_china_cpi_monthly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'cpi_monthly_cn_current',
            '预测值': 'cpi_monthly_cn_predict',
            '前值': 'cpi_monthly_cn_previous'
        }
        need_clip = True
    elif instrument == 'PPI-CN':
        df = ak.macro_china_ppi_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'ppi_cn_current',
            '预测值': 'ppi_cn_predict',
            '前值': 'ppi_cn_previous'
        }
        need_clip = True
    elif instrument == 'EXP-CN':
        df = ak.macro_china_exports_yoy()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'exp_cn_current',
            '预测值': 'exp_cn_predict',
            '前值': 'exp_cn_previous'
        }
        need_clip = True
    elif instrument == 'IMP-CN':
        df = ak.macro_china_imports_yoy()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'imp_cn_current',
            '预测值': 'imp_cn_predict',
            '前值': 'imp_cn_previous'

        }
        need_clip = True
    elif instrument == 'industrial-production-yoy-CN':
        df = ak.macro_china_industrial_production_yoy()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'ipy_cn_current',
            '预测值': 'ipy_cn_predict',
            '前值': 'ipy_cn_previous'
        }
        need_clip = True
    elif instrument == 'PMI-CN':
        df = ak.macro_china_pmi_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'pmi_cn_current',
            '预测值': 'pmi_cn_predict',
            '前值': 'pmi_cn_previous'
        }
        need_clip = True
    elif instrument == 'non-man-PMI-CN':
        df = ak.macro_china_non_man_pmi()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'nPMI_cn_current',
            '预测值': 'nPMI_cn_predict',
            '前值': 'nPMI_cn_previous'
        }
        need_clip = True
    elif instrument == 'fx-CN':
        df = ak.macro_china_fx_reserves_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'fx_cn_current',
            '预测值': 'fx_cn_predict',
            '前值': 'fx_cn_previous'
        }
        need_clip = True
    elif instrument == 'M2-CN':
        df = ak.macro_china_m2_yearly()
        df['date'] = pd.to_datetime(df['日期']).dt.date
        extract_columns = {
            '今值': 'm2_cn_current',
            '预测值': 'm2_cn_predict',
            '前值': 'm2_cn_previous'
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


def get_bond_info(code):
    prefixes = ['sh', 'sz', 'yhj']
    for pre in prefixes:
        url = f'http://money.finance.sina.com.cn/bond/info/{pre}{code}.html'
        response = requests.get(url, headers={
            'Host': 'money.finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'ULV=1704986152041:4:1:1:108.181.31.90_1701758545.440556:1701758543998; SINAGLOBAL=108.181.31.90_1690627573.870769; U_TRS1=0000005a.3c6b79c7f.64c4edfc.217210c9; UOR=,,; FIN_ALL_VISITED=sh019709%2CAU0; NEWESTVISITED_FUTURE=%7B%22code%22%3A%22AU0%22%2C%22hqcode%22%3A%22nf_AU0%22%2C%22type%22%3A1%7D; SFA_version7.26.0=2024-10-13%2018%3A03; SFA_version7.26.0_click=1; Apache=108.181.31.90_1701758545.440556; U_TRS2=0000000e.ab96375c.663674a2.1253d154; hqEtagMode=1; VISITED_BOND=sh019709; sinaH5EtagStatus=y',
            'Upgrade-Insecure-Requests': '1'
        })
        html = response.text
        if '403 Forbidden' in html:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        res = {}
        for tr in trs:
            tds = tr.find_all('td')
            key, value = tds[0].text, tds[1].text
            if key in ['债券名称', '债券简称', '债券类型', '信用等级']:
                res[key] = value
        return res


def _get_a_stock_info(code):
    url = f'https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_BASIC_ORGINFO&columns=ALL&quoteColumns=&filter=(SECURITY_CODE="{code}")&pageNumber=1&pageSize=1&sortTypes=&sortColumns=&source=HSF10&client=PC&v=06067307092909199'
    header = {
        'Host': 'datacenter.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://emweb.securities.eastmoney.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://emweb.securities.eastmoney.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
    }

    response = requests.get(url, headers=header)
    json = response.json()
    data = json['result']['data'][0]
    return {
        '股票简称': data['SECURITY_NAME_ABBR'],
        '公司名称': data['ORG_NAME'],
        '所在市场': 'A股',
        '所属行业': data['EM2016']
    }

def _get_hk_stock_info(code):
    url = f'https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_HKF10_INFO_ORGPROFILE&columns=SECUCODE,SECURITY_CODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,FOUND_DATE,CHAIRMAN,SECRETARY,ACCOUNT_FIRM,REG_ADDRESS,ADDRESS,YEAR_SETTLE_DAY,EMP_NUM,ORG_TEL,ORG_FAX,ORG_EMAIL,ORG_WEB,ORG_PROFILE,REG_PLACE&quoteColumns=&filter=(SECURITY_CODE="{code}")&pageNumber=1&pageSize=200&sortTypes=&sortColumns=&source=F10&client=PC&v=024356444940631528'
    header = {
        'Host': 'datacenter.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://emweb.securities.eastmoney.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://emweb.securities.eastmoney.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    response = requests.get(url, headers=header)
    json = response.json()
    data = json['result']['data'][0]
    return {
        '股票代码': data['SECURITY_CODE'],
        '股票简称': '',
        '公司名称': data['ORG_NAME'],
        '所在市场': '港股',
        '所属行业': data['BELONG_INDUSTRY']
    }

def _get_us_stock_info(code):
    url = f'https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_USF10_INFO_SECURITYINFO;RPT_USF10_INFO_ORGPROFILE&columns=SECUCODE,SECURITY_CODE,SECURITY_TYPE,LISTING_DATE,TRADE_MARKET,ISSUE_PRICE,ISSUE_NUM,@SECUCODE;@SECUCODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,FOUND_DATE,CHAIRMAN,ADDRESS,ORG_WEB&quoteColumns=&filter=(SECURITY_CODE="{code}")&pageNumber=1&pageSize=200&sortTypes=&sortColumns=&source=SECURITIES&client=PC&v=06687014516259584'
    header = {
        'Host': 'datacenter.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://emweb.securities.eastmoney.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://emweb.securities.eastmoney.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    response = requests.get(url, headers=header)
    json = response.json()
    data = json['result']['data'][0]
    return {
        '股票代码': data['SECURITY_CODE'],
        '股票简称': data['ORG_EN_ABBR'],
        '公司名称': data['ORG_NAME'],
        '所在市场': '美股',
        '所属行业': data['BELONG_INDUSTRY']
    }

def get_stock_info(code):
    if len(code) == 6 and (code.startswith('6') or code.startswith('0') or code.startswith('3')):
        return _get_a_stock_info(code)
    elif len(code) == 5 and code.isdigit():
        return _get_hk_stock_info(code)
    else:
        return _get_us_stock_info(code)


if __name__ == '__main__':
    print(get_market_data('AFRE-CN', '20210101', '20220110'))