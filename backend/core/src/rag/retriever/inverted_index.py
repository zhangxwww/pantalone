import logging

from rich.progress import track
from loguru import logger

from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD, DATETIME
from jieba.analyse import ChineseAnalyzer

from rag.type import Document
from rag.mixin.json_manager import DocumentMetaDataJsonManagerMixin
from rag.mixin.document_loader import DocumentLoaderMixin

from libs.utils.path import get_rag_inverted_index_path, get_rag_inverted_index_json_path, get_rag_metadata_json_path, get_rag_processed_path


logging.getLogger('jieba').disabled = True


class InvertedIndex(
    DocumentMetaDataJsonManagerMixin,
    DocumentLoaderMixin
):
    def __init__(self):
        self.path = get_rag_inverted_index_path()
        self._load_db()
        self.json_path = get_rag_inverted_index_json_path()
        self.reference_json_path = get_rag_metadata_json_path()
        self.storage_list = self.load_json()
        super().__init__()

    def update(self):
        updated = self.get_update_list(self.storage_list)
        documents = self.load_documents(updated, get_rag_processed_path())

        self.add_documents(documents)

    def add_documents(self, docs: list[Document]):
        added = False
        writer = self.ix.writer()
        for doc in track(docs, description='Indexing'):
            if doc.content:
                writer.update_document(
                    **doc.metadata.model_dump(),
                    content=doc.content,
                )
                added = True
                self.storage_list.append(doc.metadata)
        if added:
            logger.info(f'Committing')
            writer.commit()
            logger.info(f'Finish committing')
            self.save_json(self.storage_list)

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
