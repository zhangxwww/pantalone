from bs4 import BeautifulSoup

from rag.parser.skip_words import SKIP_WORDS


def parse_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    res = [p.text.strip() for p in soup.find_all('p') if not p.find('a')]
    res = [p for p in res if p and not any(kw in p for kw in SKIP_WORDS)]
    return '\n'.join(res)
