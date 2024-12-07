import os
import re
import json
import datetime

import requests
from bs4 import BeautifulSoup

from rag.type import DocumentMetaData
from rag.crawler.headers import BCF_HEADER, REPORT_HEADER, REPORT_DETAIL_HEADER, NEWS_HEADER, NEWS_DETAIL_HEADER
from libs.utils.path import get_temp_path


def _check_status_code(response, url):
    if response.status_code != 200:
        raise ValueError(f'Failed to get report list from {url} (status code: {response.status_code})')

def get_bank_or_currency_or_future_news_list(page, category):

    _CID = {
        'bank': 56684,
        'currency': 56982,
        'future': 56988
    }

    if page <= 0 or page > 20:
        raise ValueError('Page should be in [1, 20]')
    url = f'https://finance.sina.com.cn/roll/index.d.html?cid={_CID[category]}&page={page}'
    res = requests.get(url, headers=BCF_HEADER)
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

def get_bcf_detail(url):
    res = requests.get(url, headers=BCF_HEADER)
    return res.text.encode('latin1').decode('utf-8')

def get_report_list(page, category):
    category2kind = {
        'industry': 'industry',
        'macro': 'macro',
        'engineer': '11'
    }
    def _filter_goods(doc):
        key_words = ['黄金', '贵金属', '有色金属', '石油', '原油', '油气', '大宗商品']
        for word in key_words:
            if word in doc.title:
                return True
        return False
    category2filter = {
        'industry': _filter_goods,
        'macro': lambda _: True,
        'engineer': _filter_goods
    }

    url = f'https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/{category2kind[category]}/index.phtml?p={page}'
    response = requests.get(url, headers=REPORT_HEADER)
    _check_status_code(response, url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    res = []
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) != 6:
            continue
        index = tds[0].text.strip()
        if not index.isdigit():
            continue
        title = tds[1].a.text.strip()
        link = tds[1].a['href']
        link = f'https:{link}'
        dt = tds[3].text.strip()
        institution = tds[4].text.strip()
        authors = tds[5].text.strip().split('/')
        cat = f'report-{category}'
        res.append(DocumentMetaData(category=cat, title=title, date=dt, authors=authors, url=link, institution=institution))

    end = len(res) == 0
    res = [doc for doc in res if category2filter[category](doc)]
    return res, url, end

def get_report_detail(url, referer):
    headers = REPORT_DETAIL_HEADER.copy()
    headers['Referer'] = referer
    response = requests.get(url, headers=headers)
    _check_status_code(response, url)
    text = response.text
    return text

def get_news_list(date: datetime.datetime, category, topk=100):
    cat2top = {
        'news': 'finance_news_0_suda',
        'money': 'finance_money_suda',
        'stock': 'finance_stock_conten_suda'
    }
    url = f'https://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat={cat2top[category]}&top_time={date.strftime("%Y%m%d")}&get_new=1&top_show_num={topk}&top_order=DESC&js_var=all_1_data'
    response = requests.get(url, headers=NEWS_HEADER)
    _check_status_code(response, url)
    text = response.text.split('= ')[1]
    data = text \
        .replace(r'\/', '/') \
        .encode().decode('unicode-escape') \
        .replace(';', '')
    data = re.sub(r'\s', '', data)
    data = re.sub(r'[\x00-\x1F\u200E\u200F\u2028\u202F]', '', data, flags=re.UNICODE)
    data = re.sub(r'("title":"[^"]*?)"([^,"]*?)"([^"]*?")', r'\1“\2”\3', data)
    data = re.sub(r'("title":"[^"]*?)"([^,"]*?)"([^"]*?")', r'\1“\2”\3', data)
    data = re.sub(r'("title":"[^"]*?)"([^,"]*?)"([^"]*?")', r'\1“\2”\3', data)
    try:
        data = json.loads(data)
    except Exception as e:
        with open(os.path.join(get_temp_path(), f'{category}_{date.strftime("%Y%m%d")}_{topk}.json'), 'w') as f:
            f.write(data)
        raise e
    res = []
    for d in data['data']:
        title = d['title']
        dt = d['create_date']
        author = []
        url = d['url']
        institution = d['media']
        cat = f'news-{category}'
        res.append(DocumentMetaData(category=cat, title=title, date=dt, authors=author, url=url, institution=institution))
    return res

def get_news_detail(url):
    response = requests.get(url, headers=NEWS_DETAIL_HEADER)
    _check_status_code(response, url)
    text = response.text.encode('iso-8859-1').decode('utf-8')
    return text
