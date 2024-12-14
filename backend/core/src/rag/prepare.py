from rag.crawler.crawler import Crawler
from rag.parser.parser import Parser
from rag.cleaner.cleaner import Cleaner
from rag.retriever.retriever import Retriever


def prepare(args):
    if args.crawl:
        crawler = Crawler()
        crawler.crawl()

    if args.parse:
        parser = Parser()
        parser.parse()

    if args.clean:
        cleaner = Cleaner()
        cleaner.clean()

    if args.store:
        retriever = Retriever(args.store_batch_size)
        store_num = args.store_num if args.store_num != -1 else None
        retriever.update(store_num)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl', action='store_true')
    parser.add_argument('--parse', action='store_true')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--store', action='store_true')
    parser.add_argument('--store-num', type=int, default=-1)
    parser.add_argument('--store-batch-size', type=int, default=32)
    args = parser.parse_args()

    prepare(args)
