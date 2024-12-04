import os
import json
import shutil
from time import sleep

from loguru import logger

from libs.utils.path import get_temp_path
from rag.crawler.sina import get_bank_or_currency_or_future_news_list, get_bank_or_currency_or_future_news_detail


class Crawler:
    def __init__(self):
        self.temp_path = get_temp_path()
        self.info_json = self._load_info_json()

    def crawl(self):
        self._crawl_bank_currency_future_news()

    def _crawl_bank_currency_future_news(self):
        n_pages = 20

        failed = []

        for category in ['bank', 'currency', 'future']:
            exists = set(info['title'] for info in self.info_json[category])
            file_dir = os.path.join(self.temp_path, category)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            for page in range(1, n_pages + 1):
                try:
                    news_list = get_bank_or_currency_or_future_news_list(page, category)
                except Exception as e:
                    logger.error(f'[{category}] Page {page} error: {e}')
                    failed.append((category, page))
                    continue

                for i, news in enumerate(news_list):
                    title = news['title']
                    if title in exists:
                        continue

                    url = news['url']
                    logger.info(f'[{category} ({page}/{n_pages})] {i + 1}/{len(news_list)} {title} from {url}')

                    if not url:
                        continue

                    id_ = len(self.info_json[category])
                    try:
                        detail = get_bank_or_currency_or_future_news_detail(url)
                    except Exception as e:
                        logger.error(f'[{category}] {i + 1}/{len(news_list)} from {url} error: {e}')
                        detail = ''
                        failed.append((category, page, title, url))
                        continue
                    with open(os.path.join(file_dir, f'{id_}.html'), 'w', encoding='utf-8') as f:
                        f.write(detail)

                    news['id'] = id_
                    news['datetime'] = news['datetime'].strftime('%Y-%m-%d')
                    exists.add(title)
                    self.info_json[category].append(news)
                    self._save_info_json()

                    sleep(0.15)

        if failed:
            logger.error('Failed list:')
            for f in failed:
                logger.error(f)

    def _load_info_json(self):
        DEFAULT_INFO_JSON = {
            'bank': [],
            'currency': [],
            'future': []
        }

        filename = os.path.join(self.temp_path, 'info.json')
        if not os.path.exists(filename):
            return DEFAULT_INFO_JSON
        shutil.copy(filename, filename + '.bak')
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except UnicodeDecodeError:
                return DEFAULT_INFO_JSON

    def _save_info_json(self):
        filename = os.path.join(self.temp_path, 'info.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.info_json, f, ensure_ascii=False, indent=4)
