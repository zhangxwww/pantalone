import os
import json
import shutil
from time import sleep

from loguru import logger

from libs.utils.path import get_rag_raw_path, get_rag_path
from rag.type import DocumentMetaData
from rag.crawler.sina import (
    get_bank_or_currency_or_future_news_list,
    get_report_list,
    get_report_detail
)


class Crawler:
    def __init__(self):
        self.rag_path = get_rag_path()
        self.raw_path = get_rag_raw_path()
        self.metadata_list = self._load_metadata_list()

    def crawl(self):
        self._crawl_report()

    def _crawl_report(self):
        file_dir = self.raw_path
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

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

                    url = report.url
                    logger.info(f'[{category} ({page})] {i + 1}/{len(report_list)} {report.title} from {url}')

                    id_ = len(self.metadata_list)
                    try:
                        detail = get_report_detail(url, referer)
                    except Exception as e:
                        logger.error(f'[{category}] {i + 1}/{len(report_list)} from {url} error: {e}')
                        detail = ''
                        failed.append((category, page, report.title, url))
                        continue
                    with open(os.path.join(file_dir, f'{id_}.html'), 'w') as f:
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
        li = [metadata.dict() for metadata in self.metadata_list]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(li, f, ensure_ascii=False, indent=4)
