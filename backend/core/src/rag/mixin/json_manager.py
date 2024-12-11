import os
import json
import shutil

from loguru import logger

from libs.utils.context_manager import RunWithoutInterrupt

from rag.type import DocumentMetaData


class DocumentMetaDataJsonManagerMixin:
    def load_json(self, *, default=None):
        default = default or []
        if not os.path.exists(self.json_path):
            return default
        shutil.copy(self.json_path, self.json_path + '.bak')
        with open(self.json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                data = [DocumentMetaData(**d) for d in data]
                return data
            except UnicodeDecodeError:
                return default

    def save_json(self, data):
        li = [metadata.model_dump() for metadata in data]
        with open(self.json_path, 'w', encoding='utf-8') as f:
            with RunWithoutInterrupt():
                json.dump(li, f, ensure_ascii=False, indent=4)

    def get_update_list(self, current_data):
        with open(self.reference_json_path, 'r', encoding='utf-8') as f:
            metadata_list = json.load(f)
        metadata_list = [DocumentMetaData(**metadata) for metadata in metadata_list]
        url_set = set(doc.url for doc in current_data)
        updated = []
        for metadata in metadata_list:
            if metadata.url not in url_set:
                updated.append(metadata)
        logger.info(f'Found {len(updated)} updated documents')
        return updated
