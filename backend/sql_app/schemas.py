from datetime import date
from typing import List

from pydantic import BaseModel


# ********** Cash Data **********

class CashDataHistoryItemBase(BaseModel):
    name: str
    amount: float
    beginningTime: date


class CashDataHistoryItemCreate(CashDataHistoryItemBase):
    pass


class CashDataHistoryItem(CashDataHistoryItemBase):
    id: int
    cash_data_history_id: int

    class Config:
        from_attributes = True


class CashDataHistoryBase(BaseModel):
    pass


class CashDataHistoryCreate(CashDataHistoryBase):
    pass


class CashDataHistory(CashDataHistoryBase):
    id: int
    histories: List[CashDataHistoryItem] = []

    class Config:
        from_attributes = True


# ********** Monetary Fund Data **********

class MonetaryFundDataHistoryItemBase(BaseModel):
    name: str
    beginningAmount: float
    beginningTime: date
    beginningShares: float
    currentAmount: float
    currentTime: date
    currentShares: float
    fastRedemption: bool
    holding: bool


class MonetaryFundDataHistoryItemCreate(MonetaryFundDataHistoryItemBase):
    pass


class MonetaryFundDataHistoryItem(MonetaryFundDataHistoryItemBase):
    id: int
    monetary_fund_data_history_id: int

    class Config:
        from_attributes = True


class MonetaryFundDataHistoryBase(BaseModel):
    pass


class MonetaryFundDataHistoryCreate(MonetaryFundDataHistoryBase):
    pass


class MonetaryFundDataHistory(MonetaryFundDataHistoryBase):
    id: int
    histories: List[MonetaryFundDataHistoryItem] = []

    class Config:
        from_attributes = True


# ********** Fixed Deposit Data **********

class FixedDepositDataHistoryItemBase(BaseModel):
    name: str
    beginningAmount: float
    beginningTime: date
    rate: float
    maturity: int


class FixedDepositDataHistoryItemCreate(FixedDepositDataHistoryItemBase):
    pass


class FixedDepositDataHistoryItem(FixedDepositDataHistoryItemBase):
    id: int
    fixed_deposit_data_history_id: int

    class Config:
        from_attributes = True


class FixedDepositDataHistoryBase(BaseModel):
    pass


class FixedDepositDataHistoryCreate(FixedDepositDataHistoryBase):
    pass


class FixedDepositDataHistory(FixedDepositDataHistoryBase):
    id: int
    histories: List[FixedDepositDataHistoryItem] = []

    class Config:
        from_attributes = True


# ********** Fund Data **********

class FundDataHistoryItemBase(BaseModel):
    name: str
    currentNetValue: float
    currentShares: float
    currentTime: date
    holding: bool
    lockupPeriod: int


class FundDataHistoryItemCreate(FundDataHistoryItemBase):
    pass


class FundDataHistoryItem(FundDataHistoryItemBase):
    id: int
    fund_data_history_id: int

    class Config:
        from_attributes = True


class FundDataHistoryBase(BaseModel):
    pass


class FundDataHistoryCreate(FundDataHistoryBase):
    pass


class FundDataHistory(FundDataHistoryBase):
    id: int
    histories: List[FundDataHistoryItem] = []

    class Config:
        from_attributes = True


# ********** CN1YR Data **********

class CN1YRDataBase(BaseModel):
    yield_1yr: float
    date: date


class CN1YRDataCreate(CN1YRDataBase):
    pass


class CN1YRData(CN1YRDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** LPR Data **********

class LPRDataBase(BaseModel):
    lpr: float
    date: date


class LPRDataCreate(LPRDataBase):
    pass


class LPRData(LPRDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** SH000001 Close Data **********

class SH000001CloseDataBase(BaseModel):
    close: float
    date: date


class SH000001CloseDataCreate(SH000001CloseDataBase):
    pass


class SH000001CloseData(SH000001CloseDataBase):
    id: int

    class Config:
        from_attributes = True
