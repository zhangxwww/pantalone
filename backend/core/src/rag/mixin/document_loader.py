import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import track

from rag.type import Document
from rag.text_splitter.simple_splitter import SimpleSplitter


class DocumentLoader:
    def __init__(self):
        self.splitter = SimpleSplitter()

    def load_document(self, metadata, path):
        with open(os.path.join(path, f'{metadata.id}.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            return []
        return [Document(metadata=metadata, content=c) for c in self.splitter.split(content) if content]

    def load_documents(self, metadata_list, path, next_chunk_id):
        documents = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.load_document,
                    metadata, path)
                for metadata in metadata_list
            ]

            n_future = len(futures)
            for future in track(as_completed(futures), description='Loading', total=n_future):
                documents.extend(future.result())
        for i, doc in enumerate(documents):
            doc.metadata.chunk_id = next_chunk_id + i
        return documents
