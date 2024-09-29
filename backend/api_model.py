from typing import Optional

from pydantic import BaseModel


class CN1YRDateData(BaseModel):
    dates: list[str]


class LPRDateData(BaseModel):
    dates: list[str]


class IndexCloseDateData(BaseModel):
    dates: list[str]


class QueryFundNameData(BaseModel):
    symbol: str


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
    symbol: str
    currentNetValue: float
    currentShares: float
    holding: bool
    lockupPeriod: int


class AddFundHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddFundData


class RefreshFundNetValueData(BaseModel):
    symbols: list[str]