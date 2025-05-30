import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from loguru import logger
from rich.progress import track

from libs.utils.path import get_rag_processed_path, get_rag_path, get_rag_raw_path
from libs.utils.context_manager import RunWithoutInterrupt
from rag.parser.html import parse_html


class Parser:
    def __init__(self):
        self.rag_path = get_rag_path()
        self.raw_path = get_rag_raw_path()
        self.processed_path = get_rag_processed_path()

    def parse(self):
        incremental = self._find_incremental()
        n_incremental = len(incremental)
        logger.info(f'Found {n_incremental} incremental files')
        failed = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._parse_file_and_save, inc) for inc in incremental]
            for future in track(as_completed(futures), total=n_incremental, description='Parsing'):
                id_, success = future.result()
                if not success:
                    failed.append(id_)
        if failed:
            logger.error(f'Failed list:')
            for f in failed:
                logger.error(f)

    def _find_incremental(self):
        raws = [os.path.splitext(f)[0] for f in os.listdir(self.raw_path)]
        processed = [os.path.splitext(f)[0] for f in os.listdir(self.processed_path)]
        incremental = list(set(raws) - set(processed))
        return incremental

    def _parse_file_and_save(self, id_):
        raw_filename = f'{id_}.html'
        processed_filename = f'{id_}.txt'

        try:
            with open(os.path.join(self.raw_path, raw_filename), 'r', encoding='utf-8') as f:
                html = f.read()
        except UnicodeDecodeError:
            with open(os.path.join(self.raw_path, raw_filename), 'r', encoding='gbk') as f:
                html = f.read()
                html = html.encode('utf-8')
        try:
            text = parse_html(html)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            logger.error(f'Parse {raw_filename} error: {e}')
            return id_, False

        with open(os.path.join(self.processed_path, processed_filename), 'w', encoding='utf-8') as f:
            with RunWithoutInterrupt():
                f.write(text)

        return id_, True
