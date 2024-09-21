import datetime
import requests
from bs4 import BeautifulSoup
import akshare as ak


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
    date = date.strftime('%Y%m%d')
    df = ak.index_zh_a_hist(symbol=code, period='daily', start_date=date, end_date=date)
    return df['收盘'][0]


if __name__ == '__main__':
    # get_china_bond_yield(datetime.datetime.now())
    # print(get_lpr())
    print(get_close('000001', datetime.datetime.strptime('2024-09-20', '%Y-%m-%d')))