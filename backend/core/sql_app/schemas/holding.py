from pydantic import BaseModel


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
