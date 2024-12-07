from rag.crawler.crawler import Crawler
from rag.parser.parser import Parser


def prepare():
    crawler = Crawler()
    crawler.crawl()

    parser = Parser()
    parser.parse()


if __name__ == '__main__':
    prepare()
