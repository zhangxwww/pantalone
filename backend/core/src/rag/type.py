from pydantic import BaseModel


class DocumentMetaData(BaseModel):
    id: int = -1
    title: str = ''
    date: str = ''
    authors: list[str] = []
    url: str = ''
    abstract: str = ''
    institution: str = ''
