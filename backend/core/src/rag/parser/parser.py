import os
import shutil

from loguru import logger

from libs.utils.path import get_temp_path, get_docs_path
from rag.parser.html import parse_html


class Parser:
    def __init__(self):
        self.temp_path = get_temp_path()
        self.docs_path = get_docs_path()

    def parse(self):
        for d in os.listdir(self.temp_path):
            if os.path.isfile(os.path.join(self.temp_path, d)):
                self._copy_json(d)
            else:
                self._parse_dir(d)

    def _copy_json(self, file):
        origin_path = os.path.join(self.temp_path, file)
        target_path = os.path.join(self.docs_path, file)
        shutil.copy(origin_path, target_path)

    def _parse_dir(self, d):
        logger.info(f'Parsing {d}')
        failed = []
        for file in os.listdir(os.path.join(self.temp_path, d)):
            success = self._parse_file_and_save(file, d)
            if not success:
                failed.append((d, file))
        if failed:
            logger.error(f'Failed list:')
            for f in failed:
                logger.error(f)

    def _parse_file_and_save(self, file, d):
        if not file.endswith('.html'):
            return False
        logger.info(f'Parsing {file}')

        with open(os.path.join(self.temp_path, d, file), 'r', encoding='utf-8') as f:
            html = f.read()

        try:
            text = parse_html(html)
        except Exception as e:
            logger.error(f'Parse {file} error: {e}')
            return False

        doc_dir = os.path.join(self.docs_path, d)
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)

        with open(os.path.join(doc_dir, f'{os.path.splitext(d)[0]}.txt'), 'w', encoding='utf-8') as f:
            f.write(text)

        return True
