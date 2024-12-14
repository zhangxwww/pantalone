import logging

from rich.progress import Progress
from pydantic import model_validator
from langchain_ollama.embeddings import OllamaEmbeddings


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

    def embed_documents_batch(self, texts):
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
                progress.update(task, advance=end - start)
        return embeddings
