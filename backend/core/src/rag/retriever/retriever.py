from concurrent.futures import ThreadPoolExecutor, wait

from rich.progress import Progress, TimeElapsedColumn

from rag.retriever.inverted_index import InvertedIndex
from rag.retriever.vector_store import VectorStore
from rag.mixin.json_manager import DocumentMetaDataJsonManager
from rag.mixin.document_loader import DocumentLoader

from libs.utils.batcher import batcher
from libs.utils.path import (
    get_rag_retriever_json_path,
    get_rag_metadata_json_path,
    get_rag_processed_path
)


class Retriever:
    def __init__(self, batch_size):
        self.batch_size = batch_size

        self.json_manager = DocumentMetaDataJsonManager(
            get_rag_retriever_json_path(),
            get_rag_metadata_json_path()
        )
        self.loader = DocumentLoader()

        self.inverted_index = InvertedIndex()
        self.vector_store = VectorStore()

        self.storage_list = self.json_manager.load_json()

    def update(self, update_num):
        updated = self.json_manager.get_update_list(self.storage_list, update_num)
        next_chunk_id = self.json_manager.get_next_chunk_id(self.storage_list)
        documents = self.loader.load_documents_into_chunks(
            updated, get_rag_processed_path(), next_chunk_id
        )
        self.add_documents(documents)

    def add_documents(self, docs):
        progress = Progress(
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            speed_estimate_period=600,
            refresh_per_second=1
        )
        with progress:
            task = progress.add_task(f"Adding documents", total=len(docs))
            with ThreadPoolExecutor(max_workers=2) as executor:
                for batch in batcher(docs, self.batch_size):
                    self.update_storage(batch, executor)
                    self.update_json(batch)
                    progress.update(task, advance=len(batch), refresh=True)

    def update_storage(self, docs, executor):
        futures = [
            executor.submit(self.inverted_index.add_documents, docs),
            executor.submit(self.vector_store.add_documents, docs)
        ]
        wait(futures)

    def update_json(self, docs):
        self.storage_list.extend([doc.metadata for doc in docs])
        self.json_manager.save_json(self.storage_list)

    def query(self, query):
        pass
