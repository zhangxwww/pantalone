from datetime import date
from typing import List

from pydantic import BaseModel


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
