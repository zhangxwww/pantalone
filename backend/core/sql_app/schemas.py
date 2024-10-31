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
    currency: str
    currencyRate: float
    beginningCurrencyRate: float
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
    symbol: str
    currentNetValue: float
    currentShares: float
    currentTime: date
    holding: bool
    lockupPeriod: int
    dividendRatio: float


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


# ********** Index Close Data **********

class IndexCloseDataBase(BaseModel):
    code: str
    close: float
    date: date


class IndexCloseDataCreate(IndexCloseDataBase):
    pass


class IndexCloseData(IndexCloseDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** Fund Name Data **********

class FundNameDataBase(BaseModel):
    symbol: str
    name: str


class FundNameDataCreate(FundNameDataBase):
    pass


class FundNameData(FundNameDataBase):
    class Config:
        from_attributes = True


# ********** Fund Holding Data **********

class FundHoldingDataBase(BaseModel):
    year: int
    quarter: int
    fund_code: str
    code: str
    name: str
    ratio: float
    type: str


class FundHoldingDataCreate(FundHoldingDataBase):
    pass


class FundHoldingData(FundHoldingDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** Holding Not Found in Spider History **********

class HoldingNotFoundInSpiderHistoryBase(BaseModel):
    code: str
    year: int
    quarter: int

class HoldingNotFoundInSpiderHistoryCreate(HoldingNotFoundInSpiderHistoryBase):
    pass

class HoldingNotFoundInSpiderHistory(HoldingNotFoundInSpiderHistoryBase):
    id: int

    class Config:
        from_attributes = True


# ********** KLine Data **********

class KLineDataBase(BaseModel):
    code: str
    date: date
    open: float
    close: float
    high: float
    low: float
    volume: float
    period: str
    market: str


class KLineDataCreate(KLineDataBase):
    pass


class KLineData(KLineDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** Market Data **********

class MarketDataBase(BaseModel):
    code: str
    date: date
    price: float


class MarketDataCreate(MarketDataBase):
    pass


class MarketData(MarketDataBase):
    id: int

    class Config:
        from_attributes = True


# ********** Stock/bond info **********

class StockInfoDataBase(BaseModel):
    code: str
    abbreviation: str
    name: str
    industry: str
    market: str


class StockInfoDataCreate(StockInfoDataBase):
    pass


class StockInfoData(StockInfoDataBase):
    id: int

    class Config:
        from_attributes = True


class BondInfoDataBase(BaseModel):
    code: str
    abbreviation: str
    name: str
    type: str
    level: str


class BondInfoDataCreate(BondInfoDataBase):
    pass


class BondInfoData(BondInfoDataBase):
    id: int

    class Config:
        from_attributes = True
