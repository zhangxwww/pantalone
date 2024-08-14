from typing import List

from pydantic import BaseModel


class CN1YRDateData(BaseModel):
    dates: List[str]


class UploadData(BaseModel):
    file: str