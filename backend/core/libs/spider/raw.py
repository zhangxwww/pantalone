import datetime

import requests
from bs4 import BeautifulSoup


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
