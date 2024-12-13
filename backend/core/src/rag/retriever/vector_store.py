import os
import logging

from loguru import logger

from nano_vectordb import NanoVectorDB

from ai.embedings import Embedding
from ai.available_models import AvailableEmbeddingModel
from libs.utils.path import (
    get_rag_inverted_index_json_path,
    get_rag_vector_db_json_path,
    get_rag_vector_db_path,
    get_rag_processed_path
)

from rag.mixin.json_manager import DocumentMetaDataJsonManagerMixin
from rag.mixin.document_loader import DocumentLoaderMixin


logging.getLogger('nano-vectordb').disabled = True


class VectorStore(
    DocumentMetaDataJsonManagerMixin,
    DocumentLoaderMixin
):
    def __init__(self):
        self.path = get_rag_vector_db_path()
        self.json_path = get_rag_vector_db_json_path()
        self.reference_json_path = get_rag_inverted_index_json_path()
        self.storage_list = self.load_json()

        self._init_emb()
        self._init_db()
        super().__init__()

    def update(self):
        updated = self.get_update_list(self.storage_list)
        documents = self.load_documents(updated, get_rag_processed_path())
        embeddings = self.get_embeddings(documents)
        self.add_data(documents, embeddings)

    def query(self):
        pass

    def _init_emb(self):
        self.embedding = Embedding(model=AvailableEmbeddingModel.BGE_M3.value)

    def _init_db(self):
        file_path = os.path.join(get_rag_vector_db_path(), 'vector_db.json')
        self.vdb = NanoVectorDB(self.embedding.dim, storage_file=file_path)

    def get_embeddings(self, docs):
        logger.info('Embedding documents')
        texts = [doc.content for doc in docs]
        return self.embedding.embed_documents(texts)

    def add_data(self, docs, embeddings):
        date = [{
            '__vector__': emb,
            **doc.metadata.model_dump()
        } for emb, doc in zip(embeddings, docs)]

        logger.info('Upserting data')
        self.vdb.upsert(date)
        self.vdb.save()
