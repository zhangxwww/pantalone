from pydantic import BaseModel


class DocumentMetaData(BaseModel):
    id: int
    title: str
    date: str
    authors: str
    url: str
    abstract: str
