import logging
from typing import Generator

from rich.progress import Progress
from pydantic import model_validator
from langchain_ollama.embeddings import OllamaEmbeddings

from libs.decorators.return_type import return_numpy_array, yield_numpy_array


logging.getLogger('httpx').disabled = True


class Embedding(OllamaEmbeddings):

    dim: int = 0
    batch_size: int = 32

    @model_validator(mode='before')
    def set_dim(cls, values):
        model = values.get('model')
        values['dim'] = {
            'bge-m3': 1024,
            'nomic-embed-text': 768
        }[model]
        return values

    @return_numpy_array
    def embed_text(self, text: str) -> list[float]:
        return super().embed_text(text)

    @return_numpy_array
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return super().embed_documents(texts)

    @return_numpy_array
    def embed_documents_batch(self, texts: list[str]) -> list[list[float]]:
        n_texts = len(texts)
        n_batch = n_texts // self.batch_size + 1
        embeddings = []
        with Progress() as progress:
            task = progress.add_task('Embedding', total=n_texts)
            for i in range(n_batch):
                start = i * self.batch_size
                end = (i + 1) * self.batch_size
                batch = texts[start:end]
                embedded_docs = self.embed_documents(batch)
                embeddings.extend(embedded_docs)
                progress.advance(task, advance=len(batch))
        return embeddings

    @yield_numpy_array
    def embed_documents_generator(self, texts: list[str]) -> Generator:
        n_texts = len(texts)
        n_batch = n_texts // self.batch_size + 1
        with Progress() as progress:
            task = progress.add_task('Embedding', total=n_texts)
            for i in range(n_batch):
                start = i * self.batch_size
                end = (i + 1) * self.batch_size
                batch = texts[start:end]
                embedded_docs = self.embed_documents(batch)
                yield embedded_docs
                progress.advance(task, advance=len(batch))
