from sqlalchemy import Column, Integer, String, Float

from sql_app.database import Base


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
