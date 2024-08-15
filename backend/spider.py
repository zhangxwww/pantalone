import requests


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
    return y


if __name__ == '__main__':
    from datetime import datetime
    get_china_bond_yield(datetime.now())