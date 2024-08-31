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


class _AddMonetaryFundData(BaseModel):
    name: str
    beginningAmount: float
    beginningTime: str
    currentAmount: float
    currentShares: float
    fastRedemption: bool
    holding: bool


class AddMonetaryFundHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddMonetaryFundData


class _AddFixedDepositData(BaseModel):
    name: str
    beginningAmount: float
    beginningTime: str
    rate: float
    maturity: int


class AddFixedDepositHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddFixedDepositData


class _AddFundData(BaseModel):
    name: str
    beginningAmount: float
    beginningTime: str
    currentAmount: float
    holding: bool
    lockupPeriod: int


class AddFundHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddFundData