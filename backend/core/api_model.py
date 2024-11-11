from typing import Optional, Literal

from pydantic import BaseModel


class CN1YRDateData(BaseModel):
    dates: list[str]


class LPRDateData(BaseModel):
    dates: list[str]


class IndexCloseDateData(BaseModel):
    dates: list[str]


class QueryFundNameData(BaseModel):
    symbol: str


class LatestCurrencyRateData(BaseModel):
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
    currency: str
    currencyRate: float
    beginningCurrencyRate: float
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
    dividendRatio: float


class AddFundHistoryData(BaseModel):
    id: Optional[int] = None
    content: _AddFundData


class RefreshFundNetValueData(BaseModel):
    symbols: list[str]


class GetFundHoldingData(BaseModel):
    symbols: list[str]


class GetFundHoldingRelevanceData(BaseModel):
    holding: dict[str, dict[str, list]]


class GetKLineData(BaseModel):
    code: str
    period: Literal['daily', 'weekly', 'monthly']
    market: Literal[
        'index-CN', 'index-HK', 'index-US', 'index-qvix',
        'future-zh'
    ]


class GetMarketData(BaseModel):
    instrument: str


class _KLinePercentileContentData(BaseModel):
    name: str
    code: str
    market: str


class _MarketPercentileContentData(BaseModel):
    name: str
    code: str
    instrument: str


class _PercentileData(BaseModel):
    isKLine: bool
    content: list[_KLinePercentileContentData | _MarketPercentileContentData]

    class Config:
        extra = 'ignore'


class _PercentilePeriodWindowData(BaseModel):
    period: Literal['daily', 'weekly', 'monthly']
    window: int


class PercentileRequestData(BaseModel):
    period_window: list[_PercentilePeriodWindowData]
    data: list[_PercentileData]


class GetStockBondInfoRequestData(BaseModel):
    stocks: list[str]
    bonds: list[str]


class GetUCPQueryResultRequestData(BaseModel):
    ucp: str
    interval: Literal['daily', 'weekly', 'monthly', 'yearly']
    func: Literal['close', 'open', 'high', 'low']
    start_date: str | None = None
    end_date: str | None = None


class ChatMessageRequestData(BaseModel):
    messages: list[dict[str, str]]
    page: str