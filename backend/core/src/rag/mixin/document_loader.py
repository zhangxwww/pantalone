import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger
from rich.progress import track

from rag.type import Document, DocumentMetaData
from rag.text_splitter.simple_splitter import SimpleSplitter


class DocumentLoader:
    def __init__(self):
        self.splitter = SimpleSplitter()

    def load_raw_document(self, metadata: DocumentMetaData, path: str) -> Document:
        with open(os.path.join(path, f'{metadata.id}.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        return Document(metadata=metadata.model_copy(deep=True), content=content)

    def load_raw_documents(self, metadata_list: list[DocumentMetaData], path: str) -> list[Document]:
        documents = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.load_raw_document, metadata, path)
                for metadata in metadata_list
            ]

            n_future = len(futures)
            for future in track(as_completed(futures), description='Loading', total=n_future):
                documents.append(future.result())
        logger.info(f'Loaded {len(documents)} documents')
        return documents

    def load_document_into_chunks(
        self,
        metadata: DocumentMetaData,
        path: str
    ) -> list[Document]:
        with open(os.path.join(path, f'{metadata.id}.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            return []
        return [Document(metadata=metadata.model_copy(deep=True), content=c) for c in self.splitter.split(content) if content]

    def load_documents_into_chunks(
        self,
        metadata_list: list[DocumentMetaData],
        path: str,
        next_chunk_id: int | None = None
    ) -> list[Document]:

        documents = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.load_document_into_chunks,
                    metadata, path)
                for metadata in metadata_list
            ]

            n_future = len(futures)
            for future in track(as_completed(futures), description='Loading', total=n_future):
                documents.extend(future.result())
        if next_chunk_id is not None:
            for i, doc in enumerate(documents):
                doc.metadata.chunk_id = next_chunk_id + i
        logger.info(f'Loaded {len(documents)} chunks')
        return documents
