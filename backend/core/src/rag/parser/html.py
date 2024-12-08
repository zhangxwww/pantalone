from bs4 import BeautifulSoup


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    res = [p.text for p in soup.find_all('p') if not p.find('a')]
    skip_keywords = set(['责任编辑', '二维码', 'Copyright', '粉丝福利', '文章来源'])
    res = [p for p in res if not any(kw in p for kw in skip_keywords)]
    return '\n'.join(res)
