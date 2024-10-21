from sqlalchemy import Boolean, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class CashDataHistoryItem(Base):
    __tablename__ = "cash_data_history_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Float)
    beginningTime = Column(Date)

    cash_data_history_id = Column(Integer, ForeignKey('cash_data_history.id'))
    cash_data_history = relationship('CashDataHistory', back_populates='histories')


class MonetaryFundDataHistoryItem(Base):
    __tablename__ = "monetary_fund_data_history_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    beginningAmount = Column(Float)
    beginningTime = Column(Date)
    beginningShares = Column(Float)
    currentAmount = Column(Float)
    currentTime = Column(Date)
    currentShares = Column(Float)
    currency = Column(String)
    currencyRate = Column(Float)
    fastRedemption = Column(Boolean)
    holding = Column(Boolean)

    monetary_fund_data_history_id = Column(Integer, ForeignKey('monetary_fund_data_history.id'))
    monetary_fund_data_history = relationship('MonetaryFundDataHistory', back_populates='histories')


class FixedDepositDataHistoryItem(Base):
    __tablename__ = "fixed_deposit_data_history_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    beginningAmount = Column(Float)
    beginningTime = Column(Date)
    rate = Column(Float)
    maturity = Column(Integer)

    fixed_deposit_data_history_id = Column(Integer, ForeignKey('fixed_deposit_data_history.id'))
    fixed_deposit_data_history = relationship('FixedDepositDataHistory', back_populates='histories')


class FundDataHistoryItem(Base):
    __tablename__ = "fund_data_history_item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    symbol = Column(String)
    currentNetValue = Column(Float)
    currentShares = Column(Float)
    currentTime = Column(Date)
    holding = Column(Boolean)
    lockupPeriod = Column(Integer)
    dividendRatio = Column(Float)

    fund_data_history_id = Column(Integer, ForeignKey('fund_data_history.id'))
    fund_data_history = relationship('FundDataHistory', back_populates='histories')


class CashDataHistory(Base):
    __tablename__ = 'cash_data_history'

    id = Column(Integer, primary_key=True, index=True)

    histories = relationship('CashDataHistoryItem', back_populates='cash_data_history')


class MonetaryFundDataHistory(Base):
    __tablename__ = 'monetary_fund_data_history'

    id = Column(Integer, primary_key=True, index=True)

    histories = relationship('MonetaryFundDataHistoryItem', back_populates='monetary_fund_data_history')


class FixedDepositDataHistory(Base):
    __tablename__ = 'fixed_deposit_data_history'

    id = Column(Integer, primary_key=True, index=True)

    histories = relationship('FixedDepositDataHistoryItem', back_populates='fixed_deposit_data_history')


class FundDataHistory(Base):
    __tablename__ = 'fund_data_history'

    id = Column(Integer, primary_key=True, index=True)

    histories = relationship('FundDataHistoryItem', back_populates='fund_data_history')


class ChinaBondYield(Base):
    __tablename__ = 'china_bond_yield'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    yield_1yr = Column(Float)


class LPR(Base):
    __tablename__ = 'lpr'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    lpr = Column(Float)


class IndexClose(Base):
    __tablename__ = 'index_close'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    date = Column(Date)
    close = Column(Float)


class FundName(Base):
    __tablename__ = 'fund_name'

    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)


class FundHolding(Base):
    __tablename__ = 'fund_holding'

    id = Column(Integer, primary_key=True, index=True)
    fund_code = Column(String)
    year = Column(Integer)
    quarter = Column(Integer)
    code = Column(String)
    name = Column(String)
    ratio = Column(Float)
    type = Column(String)


class HoldingNotFoundInSpiderHistory(Base):
    __tablename__ = 'spider_not_found_history'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    year = Column(Integer)
    quarter = Column(Integer)


class KLineData(Base):
    __tablename__ = 'kline_data'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    date = Column(Date)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    period = Column(String)
    market = Column(String)


class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    date = Column(Date)
    price = Column(Float)