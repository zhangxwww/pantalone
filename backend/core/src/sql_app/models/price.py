from sqlalchemy import Column, Integer, String, Float, Date

from sql_app.database import Base


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