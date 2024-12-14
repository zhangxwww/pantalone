import os

from rich.progress import track
from loguru import logger

from rag.mixin.json_manager import DocumentMetaDataJsonManager
from rag.mixin.document_loader import DocumentLoader

from libs.utils.path import get_rag_metadata_json_path, get_rag_processed_path


class Cleaner:
    def __init__(self):
        self.manager = DocumentMetaDataJsonManager(get_rag_metadata_json_path(), None)
        self.loader = DocumentLoader()

    def clean(self):
        metadata_list = self.manager.load_json()
        documents = self.loader.load_raw_documents(metadata_list, get_rag_processed_path())
        cleaned_metadata_list = []
        for doc in documents:
            if doc.content:
                cleaned_metadata_list.append(doc.metadata)

        empty_docs = [doc for doc in documents if not doc.content]
        logger.info(f'Found {len(empty_docs)} empty documents')
        for doc in track(empty_docs, description='Cleaning'):
            path = os.path.join(get_rag_processed_path(), f'{doc.metadata.id}.txt')
            os.remove(path)

        self.manager.save_json(cleaned_metadata_list)
