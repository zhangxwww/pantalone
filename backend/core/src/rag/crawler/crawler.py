import os
import json
import shutil
import datetime
from time import sleep

from loguru import logger

from libs.utils.path import get_rag_raw_path, get_rag_path
from libs.utils.date_transform import get_dates_between_str
from rag.type import DocumentMetaData
from rag.crawler.sina import (
    get_report_list,
    get_report_detail,
    get_news_list,
    get_news_detail
)


class Crawler:
    def __init__(self, earlist_news_date='2020-01-01'):
        self.rag_path = get_rag_path()
        self.raw_path = get_rag_raw_path()
        self.metadata_list = self._load_metadata_list()
        self.earlist_news_date = earlist_news_date

    def crawl(self):
        self._crawl_report()
        self._crawl_news()

    def _crawl_report(self):
        failed = []
        exists = set([info.url for info in self.metadata_list])
        for category in ['industry', 'macro', 'engineer']:

            page = 1
            n_continue_exists = 0
            should_break = False
            while not should_break:
                logger.info(f'[{category}] page {page}')
                try:
                    report_list, referer, done = get_report_list(page, category)
                    if done or page > 200:
                        break
                except Exception as e:
                    logger.error(f'[{category}] page {page} error: {e}')
                    failed.append((category, page))
                    continue

                for i, report in enumerate(report_list):
                    url = report.url
                    if not url:
                        continue
                    if url in exists:
                        n_continue_exists += 1
                        if n_continue_exists >= 3:
                            should_break = True
                            break
                        continue

                    id_ = len(self.metadata_list)
                    try:
                        detail = get_report_detail(url, referer)
                    except Exception as e:
                        logger.error(f'[{category}] {i + 1}/{len(report_list)} from {url} error: {e}')
                        detail = ''
                        failed.append((category, page, report.title, url))
                        continue
                    with open(os.path.join(self.raw_path, f'{id_}.html'), 'w') as f:
                        f.write(detail)

                    report.id = id_
                    exists.add(url)
                    self.metadata_list.append(report)
                    self._save_metadata_list()

                    sleep(0.3)
                page += 1

        if failed:
            logger.error('Failed list:')
            for f in failed:
                logger.error(f)

    def _crawl_news(self, topk=20):
        failed = []
        exists = set([info.url for info in self.metadata_list])

        latest_date = self._get_latest_news_date()
        current_date = datetime.datetime.now() - datetime.timedelta(days=1)
        current_date = current_date.strftime('%Y-%m-%d')
        dates_between = get_dates_between_str(latest_date, current_date)
        for date in dates_between:
            for category in ['news', 'money', 'stock']:
                logger.info(f'[{category}] {date.strftime("%Y-%m-%d")}')
                try:
                    news_list = get_news_list(date, category, topk=topk)
                except Exception as e:
                    logger.error(f'[{category}] ({topk}) error: {e}')
                    failed.append((category, date.strftime("%Y-%m-%d"), topk))
                    try:
                        news_list = get_news_list(date, category, topk=topk // 2)
                    except:
                        logger.error(f'[{category}] ({topk // 2}) error: {e}')
                        failed.append((category, date.strftime("%Y-%m-%d"), topk // 2))
                        continue
                for i, news in enumerate(news_list):
                    url = news.url
                    if not url or url in exists:
                        continue

                    id_ = len(self.metadata_list)
                    try:
                        detail = get_news_detail(url)
                    except Exception as e:
                        logger.error(f'[{category}] {i + 1}/{len(news_list)} from {url} error: {e}')
                        detail = ''
                        failed.append((category, news.title, url))
                        continue
                    with open(os.path.join(self.raw_path, f'{id_}.html'), 'w', encoding='utf-8') as f:
                        f.write(detail)

                    news.id = id_
                    exists.add(url)
                    self.metadata_list.append(news)
                    self._save_metadata_list()

        if failed:
            logger.error('Failed list:')
            for f in failed:
                logger.error(f)

    def _get_latest_news_date(self):
        dates = [metadata.date for metadata in self.metadata_list if metadata.category.startswith('news-') and metadata.date]
        if not dates:
            return self.earlist_news_date
        dates = sorted(dates, reverse=True)
        return dates[0]

    def _load_metadata_list(self):
        DEFAULT_metadata_list = []

        filename = os.path.join(self.rag_path, 'metadata.json')
        if not os.path.exists(filename):
            return DEFAULT_metadata_list
        shutil.copy(filename, filename + '.bak')
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                data = [DocumentMetaData(**d) for d in data]
                return data
            except UnicodeDecodeError:
                return DEFAULT_metadata_list

    def _save_metadata_list(self):
        filename = os.path.join(self.rag_path, 'metadata.json')
        li = [metadata.model_dump() for metadata in self.metadata_list]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(li, f, ensure_ascii=False, indent=4)
        except KeyboardInterrupt:
            pass
