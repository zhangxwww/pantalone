import datetime

from libs.utils.date_transform import get_dates_between_str

from rag.crawler.crawler import Crawler
from rag.parser.parser import Parser


def prepare(dates):
    crawler = Crawler()
    crawler.crawl()

    parser = Parser()
    parser.parse()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=str, default='')
    parser.add_argument('--end', type=str, default='')
    args = parser.parse_args()

    start = args.start or datetime.datetime.now().strftime('%Y-%m-%d')
    end = args.end or datetime.datetime.now().strftime('%Y-%m-%d')
    dates = get_dates_between_str(start, end)

    prepare(dates)
