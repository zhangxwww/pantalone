import datetime

import requests
from bs4 import BeautifulSoup


_HEADER = {
    'Host': 'finance.sina.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

_CID = {
    'bank': 56684,
    'currency': 56982,
    'future': 56988
}

def get_bank_or_currency_or_future_news_list(page, category):
    if page <= 0 or page > 20:
        raise ValueError('Page should be in [1, 20]')
    url = f'https://finance.sina.com.cn/roll/index.d.html?cid={_CID[category]}&page={page}'
    res = requests.get(url, headers=_HEADER)
    s = BeautifulSoup(res.text, 'html.parser')
    ul = s.select('#listcontent')[0]
    lis = ul.find_all('li')

    res = []
    for li in lis:
        title_date = li.text.encode('latin1').decode('utf-8').strip()
        last_left_bracket = title_date.rfind('(')
        if last_left_bracket != -1:
            title = title_date[:last_left_bracket].strip()
            dt = title_date[last_left_bracket + 1:-1]
            dt = datetime.datetime.strptime(dt, '%m月%d日 %H:%M')
            dt = dt.replace(year=datetime.datetime.now().year)
            if dt > datetime.datetime.now():
                dt = dt.replace(year=datetime.datetime.now().year - 1)
        else:
            title = title_date
            dt = datetime.datetime.now()
        a = li.find('a')
        url = a['href'] if a else ''
        res.append({'title': title, 'url': url, 'datetime': dt})
    return res


def get_bank_or_currency_or_future_news_detail(url):
    res = requests.get(url, headers=_HEADER)
    return res.text.encode('latin1').decode('utf-8')
