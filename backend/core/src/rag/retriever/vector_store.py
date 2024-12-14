import os
import logging

from nano_vectordb import NanoVectorDB

from ai.embedings import Embedding
from ai.available_models import AvailableEmbeddingModel
from libs.utils.path import (
    get_rag_vector_db_path,
)


logging.getLogger('nano-vectordb').disabled = True


class VectorStore:
    def __init__(self):
        self.path = get_rag_vector_db_path()
        self._init_emb()
        self._init_db()

    def add_documents(self, docs):
        embedding = self.embedding.embed_documents([doc.content for doc in docs])
        self.add_data(docs, embedding)

    def query(self):
        pass

    def _init_emb(self):
        self.embedding = Embedding(model=AvailableEmbeddingModel.BGE_M3.value)

    def _init_db(self):
        file_path = os.path.join(get_rag_vector_db_path(), 'vector_db.json')
        self.vdb = NanoVectorDB(self.embedding.dim, storage_file=file_path)

    def add_data(self, docs, embeddings):
        assert len(docs) == len(embeddings)
        data = [{
            '__id__': doc.metadata.chunk_id,
            '__vector__': emb,
            **doc.metadata.model_dump()
        } for emb, doc in zip(embeddings, docs)]

        self.vdb.upsert(data)
        self.vdb.save()
