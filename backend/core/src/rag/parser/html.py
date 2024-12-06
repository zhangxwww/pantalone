from bs4 import BeautifulSoup


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    res = [p.text for p in soup.find_all('p') if not p.find('a')]
    return '\n'.join(res)
