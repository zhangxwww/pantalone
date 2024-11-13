from pydantic import BaseModel


# ********** Fund Name Data **********

class FundNameDataBase(BaseModel):
    symbol: str
    name: str


class FundNameDataCreate(FundNameDataBase):
    pass


class FundNameData(FundNameDataBase):
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
