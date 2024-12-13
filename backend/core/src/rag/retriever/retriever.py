from rag.retriever.inverted_index import InvertedIndex
from rag.retriever.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.inverted_index = InvertedIndex()
        self.vector_store = VectorStore()

    def update(self):
        self.inverted_index.update()
        self.vector_store.update()

    def retrieve(self, query):
        pass