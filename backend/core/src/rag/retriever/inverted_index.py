import os
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

from rich.progress import track
from loguru import logger

from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD, DATETIME
from jieba.analyse import ChineseAnalyzer

from rag.type import Document, DocumentMetaData
from rag.text_splitter.simple_splitter import SimpleSplitter

from libs.utils.path import get_rag_inverted_index_path, get_rag_inverted_index_json_path, get_rag_metadata_json_path, get_rag_processed_path
from libs.utils.run_manager import RunWithoutInterrupt


class InvertedIndex:
    def __init__(self):
        self.path = get_rag_inverted_index_path()
        self._load_db()
        self.storage_list = self._load_storage_json()
        self.splitter = SimpleSplitter()

    def update(self):
        updated = self.get_updated_metadata_list()
        documents = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.load_document, metadata) for metadata in updated]
            n_future = len(futures)
            for future in track(as_completed(futures, timeout=10), description='Loading', total=n_future):
                try:
                    documents.extend(future.result())
                except TimeoutError:
                    pass

        timeout_doc_id = set(u.id for u in updated) - set(d.metadata.id for d in documents)
        if timeout_doc_id:
            logger.error('Timeout list:')
            for i in timeout_doc_id:
                logger.error(f'{i}')

        self.add_documents(documents)

    def get_updated_metadata_list(self):
        with open(get_rag_metadata_json_path(), 'r', encoding='utf-8') as f:
            metadata_list = json.load(f)
        metadata_list = [DocumentMetaData(**metadata) for metadata in metadata_list]
        storage_url_set = set(doc.url for doc in self.storage_list)
        updated = []
        for metadata in metadata_list:
            if metadata.url not in storage_url_set:
                updated.append(metadata)
        logger.info(f'Found {len(updated)} updated documents')
        return updated

    def load_document(self, metadata):
        path = get_rag_processed_path()
        with open(os.path.join(path, f'{metadata.id}.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            return []
        docs = [Document(metadata=metadata, content=c) for c in self.splitter.split(content)]
        return [doc for doc in docs if doc.content]

    def add_documents(self, docs: list[Document]):
        writer = self.ix.writer()
        for doc in track(docs, description='Indexing'):
            if doc.content:
                writer.update_document(
                    **doc.metadata.model_dump(),
                    content=doc.content,
                )
                self.storage_list.append(doc.metadata)
        logger.info(f'Committing')
        writer.commit()
        logger.info(f'Finish committing')
        self._save_storage_list()

    def query(self):
        pass

    def _load_db(self):
        try:
            logger.info('Loading inverted index')
            self.ix = open_dir(self.path)
        except EmptyIndexError:
            self._create()

    def _create(self):
        logger.info('Creating inverted index')
        schema = Schema(
            id=STORED,
            category=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            date=DATETIME(stored=True),
            authors=KEYWORD(stored=True),
            url=ID(stored=True, unique=True),
            abstract=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            institution=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
        )
        self.ix = create_in(self.path, schema)

    def _load_storage_json(self):
        DEFAULT_STORAGE_LIST = []

        filename = get_rag_inverted_index_json_path()
        if not os.path.exists(filename):
            return DEFAULT_STORAGE_LIST
        shutil.copy(filename, filename + '.bak')
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                data = [DocumentMetaData(**d) for d in data]
                return data
            except UnicodeDecodeError:
                return DEFAULT_STORAGE_LIST

    def _save_storage_list(self):
        filename = get_rag_inverted_index_json_path()
        li = [metadata.model_dump() for metadata in self.storage_list]
        with open(filename, 'w', encoding='utf-8') as f:
            with RunWithoutInterrupt():
                json.dump(li, f, ensure_ascii=False, indent=4)
