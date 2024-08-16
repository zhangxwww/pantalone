from typing import List, Optional

from pydantic import BaseModel


class CN1YRDateData(BaseModel):
    dates: List[str]


class UploadData(BaseModel):
    file: str


class _AddCashData(BaseModel):
    name: str
    amount: float


class AddCashHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddCashData