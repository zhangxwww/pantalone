import logging

from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD, DATETIME
from jieba.analyse import ChineseAnalyzer

from rag.type import Document

from libs.utils.path import get_rag_inverted_index_path


logging.getLogger('jieba').disabled = True


class InvertedIndex:
    def __init__(self):
        self.path = get_rag_inverted_index_path()
        self._load_db()

    def add_documents(self, docs: list[Document]):
        writer = self.ix.writer()
        docs = [doc for doc in docs if doc.content]
        if docs:
            for doc in docs:
                metadata = doc.metadata.model_dump()
                metadata['chunk_id'] = str(metadata['chunk_id'])
                writer.update_document(
                    **metadata,
                    content=doc.content,
                )
            writer.commit()

    def query(self):
        pass

    def _load_db(self):
        try:
            self.ix = open_dir(self.path)
        except EmptyIndexError:
            self._create()

    def _create(self):
        schema = Schema(
            id=STORED,
            chunk_id=ID(stored=True, unique=True),
            category=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            date=DATETIME(stored=True),
            authors=KEYWORD(stored=True),
            url=STORED,
            abstract=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            institution=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
        )
        self.ix = create_in(self.path, schema)
