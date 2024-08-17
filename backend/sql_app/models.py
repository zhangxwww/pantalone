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
    currentAmount = Column(Float)
    currentTime = Column(Date)
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
    beginningAmount = Column(Float)
    beginningTime = Column(Date)
    currentAmount = Column(Float)
    currentTime = Column(Date)
    holding = Column(Boolean)
    lockupPeriod = Column(Integer)

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