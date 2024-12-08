import os
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import track

from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD, DATETIME

from rag.type import Document, DocumentMetaData
from rag.text_split.simple_splitter import SimpleSplitter

from libs.utils.path import get_rag_inverted_index_path, get_rag_storage_json_path, get_rag_metadata_json_path, get_rag_processed_path
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
            for doc in track(as_completed(futures), description='Loading'):
                documents.extend(doc)
        self.add_documents(documents)

    def get_updated_metadata_list(self):
        metadata_list = json.load(get_rag_metadata_json_path())
        storage_url_set = set(doc.url for doc in self.storage_list)
        updated = []
        for metadata in metadata_list:
            if metadata.url not in storage_url_set:
                updated.append(metadata)
        return updated

    def load_document(self, metadata):
        path = get_rag_processed_path()
        with open(os.path.join(path, f'{metadata.id}.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        return [Document(metadata=metadata, content=c) for c in self.splitter.split(content)]

    def add_documents(self, docs: list[Document]):
        writer = self.ix.writer()
        for doc in track(docs, description='Indexing'):
            if doc.content:
                writer.update_document(
                    **doc.metadata.model_dump(),
                    content=doc.content,
                )
                self.storage_list.append(doc.metadata)
        writer.commit()
        self._save_storage_list()

    def query(self):
        pass

    def _load_db(self):
        try:
            self.ix = open_dir(self.path)
        except EmptyIndexError:
            self._create()

    def _create(self):
        schema = Schema(
            raw_id=STORED,
            caterogy=TEXT(stored=True),
            title=TEXT(stored=True),
            date=DATETIME(stored=True),
            authors=KEYWORD(stored=True),
            url=ID(stored=True, unique=True),
            abstract=TEXT(stored=True),
            institution=TEXT(stored=True),
            content=TEXT(stored=True),
        )
        self.ix = create_in(self.path, schema)

    def _load_storage_json(self):
        DEFAULT_STORAGE_LIST = []

        filename = get_rag_storage_json_path()
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
        filename = get_rag_storage_json_path()
        li = [metadata.model_dump() for metadata in self.storage_list]
        with open(filename, 'w', encoding='utf-8') as f:
            with RunWithoutInterrupt():
                json.dump(li, f, ensure_ascii=False, indent=4)
