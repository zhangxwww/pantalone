from rag.crawler.crawler import Crawler
from rag.parser.parser import Parser
from rag.retriever.retriever import Retriever


def prepare(args):
    if args.crawl:
        crawler = Crawler()
        crawler.crawl()

    if args.parse:
        parser = Parser()
        parser.parse()

    if args.store:
        retriever = Retriever()
        retriever.update()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl', action='store_true')
    parser.add_argument('--parse', action='store_true')
    parser.add_argument('--store', action='store_true')
    args = parser.parse_args()

    prepare(args)
