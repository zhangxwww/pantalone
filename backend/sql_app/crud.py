from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas

# ********** get all history **********

def get_all_cash_data_history(db: Session):
    return db.query(models.CashDataHistory).all()

def get_all_monetary_fund_data_history(db: Session):
    return db.query(models.MonetaryFundDataHistory).all()

def get_all_fixed_deposit_data_history(db: Session):
    return db.query(models.FixedDepositDataHistory).all()

def get_all_fund_data_history(db: Session):
    return db.query(models.FundDataHistory).all()


# ********** get history by id **********

def get_cash_data_history_by_id(
    db: Session,
    cash_data_history_id: int
):
    return db.query(models.CashDataHistory).filter(models.CashDataHistory.id == cash_data_history_id).one()

def get_monetary_fund_data_history_by_id(
    db: Session,
    monetary_fund_data_history_id: int
):
    return db.query(models.MonetaryFundDataHistory).filter(models.MonetaryFundDataHistory.id == monetary_fund_data_history_id).one()

def get_fixed_deposit_data_history_by_id(
    db: Session,
    fixed_deposit_data_history_id: int
):
    return db.query(models.FixedDepositDataHistory).filter(models.FixedDepositDataHistory.id == fixed_deposit_data_history_id).one()

def get_fund_data_history_by_id(
    db: Session,
    fund_data_history_id: int
):
    return db.query(models.FundDataHistory).filter(models.FundDataHistory.id == fund_data_history_id).one()

# ********** get history item by history id and order by date **********

def get_cash_data_history_item_by_history_id(
    db: Session,
    cash_data_history_id: int
):
    return db.query(models.CashDataHistoryItem) \
        .filter(models.CashDataHistoryItem.cash_data_history_id == cash_data_history_id) \
        .order_by(models.CashDataHistoryItem.beginningTime) \
        .all()

def get_monetary_fund_data_history_item_by_history_id(
    db: Session,
    monetary_fund_data_history_id: int
):
    return db.query(models.MonetaryFundDataHistoryItem) \
        .filter(models.MonetaryFundDataHistoryItem.monetary_fund_data_history_id == monetary_fund_data_history_id) \
        .order_by(models.MonetaryFundDataHistoryItem.currentTime) \
        .all()

def get_fixed_deposit_data_history_item_by_history_id(
    db: Session,
    fixed_deposit_data_history_id: int
):
    return db.query(models.FixedDepositDataHistoryItem) \
        .filter(models.FixedDepositDataHistoryItem.fixed_deposit_data_history_id == fixed_deposit_data_history_id) \
        .order_by(models.FixedDepositDataHistoryItem.beginningTime) \
        .all()

def get_fund_data_history_item_by_history_id(
    db: Session,
    fund_data_history_id: int
):
    return db.query(models.FundDataHistoryItem) \
        .filter(models.FundDataHistoryItem.fund_data_history_id == fund_data_history_id) \
        .order_by(models.FundDataHistoryItem.currentTime) \
        .all()

# ********** create history **********

def create_cash_data_history(
    db: Session,
    cash_data_history: schemas.CashDataHistoryCreate
):
    db_cash_data_history = models.CashDataHistory(**cash_data_history.model_dump())
    db.add(db_cash_data_history)
    db.commit()
    db.refresh(db_cash_data_history)
    return db_cash_data_history

def create_monetary_fund_data_history(db: Session, monetary_fund_data_history: schemas.MonetaryFundDataHistoryCreate):
    db_monetary_fund_data_history = models.MonetaryFundDataHistory(**monetary_fund_data_history.model_dump())
    db.add(db_monetary_fund_data_history)
    db.commit()
    db.refresh(db_monetary_fund_data_history)
    return db_monetary_fund_data_history

def create_fixed_deposit_data_history(db: Session, fixed_deposit_data_history: schemas.FixedDepositDataHistoryCreate):
    db_fixed_deposit_data_history = models.FixedDepositDataHistory(**fixed_deposit_data_history.model_dump())
    db.add(db_fixed_deposit_data_history)
    db.commit()
    db.refresh(db_fixed_deposit_data_history)
    return db_fixed_deposit_data_history

def create_fund_data_history(db: Session, fund_data_history: schemas.FundDataHistoryCreate):
    db_fund_data_history = models.FundDataHistory(**fund_data_history.model_dump())
    db.add(db_fund_data_history)
    db.commit()
    db.refresh(db_fund_data_history)
    return db_fund_data_history

# ********** create history item **********

def create_cash_data_history_item(
    db: Session,
    cash_data_history_item: schemas.CashDataHistoryItemCreate,
    cash_data_history_id: Optional[int] = None
):
    if cash_data_history_id is None or not db.query(models.CashDataHistory).filter(models.CashDataHistory.id == cash_data_history_id).first():
        history = create_cash_data_history(db, schemas.CashDataHistoryCreate())
        cash_data_history_id = history.id

    db_cash_data_history_item = models.CashDataHistoryItem(**cash_data_history_item.model_dump())
    db_cash_data_history_item.cash_data_history_id = cash_data_history_id
    db.add(db_cash_data_history_item)
    db.commit()
    db.refresh(db_cash_data_history_item)
    return db_cash_data_history_item

def create_monetary_fund_data_history_item(
    db: Session,
    monetary_fund_data_history_item: schemas.MonetaryFundDataHistoryItemCreate,
    monetary_fund_data_history_id: Optional[int] = None
):
    if monetary_fund_data_history_id is None or not db.query(models.MonetaryFundDataHistory).filter(models.MonetaryFundDataHistory.id == monetary_fund_data_history_id).first():
        history = create_monetary_fund_data_history(db, schemas.MonetaryFundDataHistoryCreate())
        monetary_fund_data_history_id = history.id

    db_monetary_fund_data_history_item = models.MonetaryFundDataHistoryItem(**monetary_fund_data_history_item.model_dump())
    db_monetary_fund_data_history_item.monetary_fund_data_history_id = monetary_fund_data_history_id
    db.add(db_monetary_fund_data_history_item)
    db.commit()
    db.refresh(db_monetary_fund_data_history_item)
    return db_monetary_fund_data_history_item

def create_fixed_deposit_data_history_item(
    db: Session,
    fixed_deposit_data_history_item: schemas.FixedDepositDataHistoryItemCreate,
    fixed_deposit_data_history_id: Optional[int] = None
):
    if fixed_deposit_data_history_id is None or not db.query(models.FixedDepositDataHistory).filter(models.FixedDepositDataHistory.id == fixed_deposit_data_history_id).first():
        history = create_fixed_deposit_data_history(db, schemas.FixedDepositDataHistoryCreate())
        fixed_deposit_data_history_id = history.id

    db_fixed_deposit_data_history_item = models.FixedDepositDataHistoryItem(**fixed_deposit_data_history_item.model_dump())
    db_fixed_deposit_data_history_item.fixed_deposit_data_history_id = fixed_deposit_data_history_id
    db.add(db_fixed_deposit_data_history_item)
    db.commit()
    db.refresh(db_fixed_deposit_data_history_item)
    return db_fixed_deposit_data_history_item

def create_fund_data_history_item(
    db: Session,
    fund_data_history_item: schemas.FundDataHistoryItemCreate,
    fund_data_history_id: Optional[int] = None
):
    if fund_data_history_id is None or not db.query(models.FundDataHistory).filter(models.FundDataHistory.id == fund_data_history_id).first():
        history = create_fund_data_history(db, schemas.FundDataHistoryCreate())
        fund_data_history_id = history.id

    db_fund_data_history_item = models.FundDataHistoryItem(**fund_data_history_item.model_dump())
    db_fund_data_history_item.fund_data_history_id = fund_data_history_id
    db.add(db_fund_data_history_item)
    db.commit()
    db.refresh(db_fund_data_history_item)
    return db_fund_data_history_item