from pydantic import model_validator
from langchain_ollama.embeddings import OllamaEmbeddings


class Embedding(OllamaEmbeddings):

    dim: int = 0

    @model_validator(mode='before')
    def set_dim(cls, values):
        model = values.get('model')
        values['dim'] = {
            'bge-m3': 1024,
            'nomic-embed-text': 768
        }[model]
        return values
