from rag.crawler.crawler import Crawler
from rag.parser.parser import Parser


def prepare(args):
    if args.crawl:
        crawler = Crawler()
        crawler.crawl()

    if args.parse:
        parser = Parser()
        parser.parse()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl', action='store_true')
    parser.add_argument('--parse', action='store_true')
    args = parser.parse_args()

    prepare(args)
