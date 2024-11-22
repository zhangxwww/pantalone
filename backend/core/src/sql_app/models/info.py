from sqlalchemy import Column, Integer, String

from sql_app.database import Base


class FundName(Base):
    __tablename__ = 'fund_name'

    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)


class StockInfoData(Base):
    __tablename__ = 'stock_info_data'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    abbreviation = Column(String)
    name = Column(String)
    industry = Column(String)
    market = Column(String)


class BondInfoData(Base):
    __tablename__ = 'bond_info_data'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    abbreviation = Column(String)
    name = Column(String)
    type = Column(String)
    level = Column(String)