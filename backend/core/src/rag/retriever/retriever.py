from rag.retriever.inverted_index import InvertedIndex


class Retriever:
    def __init__(self):
        self.inverted_index = InvertedIndex()

    def update(self):
        self.inverted_index.update()

    def retrieve(self, query):
        pass