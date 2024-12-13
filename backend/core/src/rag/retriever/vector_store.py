import os

from nano_vectordb import NanoVectorDB

from ai.embedings import Embedding
from ai.available_models import AVAILABLE_EMBEDDING_MODELS
from libs.utils.path import (
    get_rag_inverted_index_json_path,
    get_rag_vector_db_json_path,
    get_rag_vector_db_path
)
from rag.mixin.json_manager import DocumentMetaDataJsonManagerMixin


class VectorStore(DocumentMetaDataJsonManagerMixin):
    def __init__(self):
        self.json_path = get_rag_vector_db_json_path()
        self.reference_json_path = get_rag_inverted_index_json_path()
        self._init_emb()
        self._init_db()

    def _init_emb(self):
        self.embedding = Embedding(model=AVAILABLE_EMBEDDING_MODELS.BGE_M3.value)

    def _init_db(self):
        file_path = os.path.join(get_rag_vector_db_path(), 'vector_db.json')
        self.vdb = NanoVectorDB(self.embedding.dim, file_path)
