from bs4 import BeautifulSoup


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    res = [p for p in soup.find_all('p') if not p.find('a') and not p.get('class')]
    return '\n'.join(res)
