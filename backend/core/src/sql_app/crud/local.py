from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from loguru import logger

from sql_app import models, schemas


# ********** get all history **********

async def get_all_cash_data_history(db: AsyncSession):
    query = select(models.CashDataHistory)
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_monetary_fund_data_history(db: AsyncSession):
    query = select(models.MonetaryFundDataHistory)
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_fixed_deposit_data_history(db: AsyncSession):
    query = select(models.FixedDepositDataHistory)
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_fund_data_history(db: AsyncSession):
    query = select(models.FundDataHistory)
    result = await db.execute(query)
    return result.scalars().all()


# ********** get history by id **********

async def get_cash_data_history_by_id(
    db: AsyncSession,
    cash_data_history_id: int
):
    query = select(models.CashDataHistory).filter(models.CashDataHistory.id == cash_data_history_id)
    result = await db.execute(query)
    return result.scalars().one()

async def get_monetary_fund_data_history_by_id(
    db: AsyncSession,
    monetary_fund_data_history_id: int
):
    query = select(models.MonetaryFundDataHistory).filter(models.MonetaryFundDataHistory.id == monetary_fund_data_history_id)
    result = await db.execute(query)
    return result.scalars().one()

async def get_fixed_deposit_data_history_by_id(
    db: AsyncSession,
    fixed_deposit_data_history_id: int
):
    query = select(models.FixedDepositDataHistory).filter(models.FixedDepositDataHistory.id == fixed_deposit_data_history_id)
    result = await db.execute(query)
    return result.scalars().one()

async def get_fund_data_history_by_id(
    db: AsyncSession,
    fund_data_history_id: int
):
    query = select(models.FundDataHistory).filter(models.FundDataHistory.id == fund_data_history_id)
    result = await db.execute(query)
    return result.scalars().one()

# ********** get history item by history id and order by date **********

async def get_cash_data_history_item_by_history_id(
    db: AsyncSession,
    cash_data_history_id: int
):
    query = select(models.CashDataHistoryItem).filter(models.CashDataHistoryItem.cash_data_history_id == cash_data_history_id).order_by(models.CashDataHistoryItem.beginningTime)
    result = await db.execute(query)
    return result.scalars().all()

async def get_monetary_fund_data_history_item_by_history_id(
    db: AsyncSession,
    monetary_fund_data_history_id: int
):
    query = select(models.MonetaryFundDataHistoryItem).filter(models.MonetaryFundDataHistoryItem.monetary_fund_data_history_id == monetary_fund_data_history_id).order_by(models.MonetaryFundDataHistoryItem.currentTime)
    result = await db.execute(query)
    return result.scalars().all()

async def get_fixed_deposit_data_history_item_by_history_id(
    db: AsyncSession,
    fixed_deposit_data_history_id: int
):
    query = select(models.FixedDepositDataHistoryItem).filter(models.FixedDepositDataHistoryItem.fixed_deposit_data_history_id == fixed_deposit_data_history_id).order_by(models.FixedDepositDataHistoryItem.beginningTime)
    result = await db.execute(query)
    return result.scalars().all()

async def get_fund_data_history_item_by_history_id(
    db: AsyncSession,
    fund_data_history_id: int
):
    query = select(models.FundDataHistoryItem).filter(models.FundDataHistoryItem.fund_data_history_id == fund_data_history_id).order_by(models.FundDataHistoryItem.currentTime)
    result = await db.execute(query)
    return result.scalars().all()

# ********** create history **********

async def create_cash_data_history(
    db: AsyncSession,
    cash_data_history: schemas.CashDataHistoryCreate
):
    db_cash_data_history = models.CashDataHistory(**cash_data_history.model_dump())
    db.add(db_cash_data_history)
    await db.commit()
    await db.refresh(db_cash_data_history)
    return db_cash_data_history

async def create_monetary_fund_data_history(db: AsyncSession, monetary_fund_data_history: schemas.MonetaryFundDataHistoryCreate):
    db_monetary_fund_data_history = models.MonetaryFundDataHistory(**monetary_fund_data_history.model_dump())
    db.add(db_monetary_fund_data_history)
    await db.commit()
    await db.refresh(db_monetary_fund_data_history)
    return db_monetary_fund_data_history

async def create_fixed_deposit_data_history(db: AsyncSession, fixed_deposit_data_history: schemas.FixedDepositDataHistoryCreate):
    db_fixed_deposit_data_history = models.FixedDepositDataHistory(**fixed_deposit_data_history.model_dump())
    db.add(db_fixed_deposit_data_history)
    await db.commit()
    await db.refresh(db_fixed_deposit_data_history)
    return db_fixed_deposit_data_history

async def create_fund_data_history(db: AsyncSession, fund_data_history: schemas.FundDataHistoryCreate):
    db_fund_data_history = models.FundDataHistory(**fund_data_history.model_dump())
    db.add(db_fund_data_history)
    await db.commit()
    await db.refresh(db_fund_data_history)
    return db_fund_data_history

# ********** create history item **********

async def create_cash_data_history_item(
    db: AsyncSession,
    cash_data_history_item: schemas.CashDataHistoryItemCreate,
    cash_data_history_id: Optional[int] = None
):
    create = False
    if cash_data_history_id is None:
        create = True
    else:
        query = select(models.CashDataHistory).filter(models.CashDataHistory.id == cash_data_history_id)
        result = await db.execute(query)
        if result.scalars().first() is None:
            create = True

    if create:
        history = await create_cash_data_history(db, schemas.CashDataHistoryCreate())
        cash_data_history_id = history.id

        logger.debug(f'create history {cash_data_history_id}')

    db_cash_data_history_item = models.CashDataHistoryItem(**cash_data_history_item.model_dump())
    db_cash_data_history_item.cash_data_history_id = cash_data_history_id
    db.add(db_cash_data_history_item)
    await db.commit()
    await db.refresh(db_cash_data_history_item)
    return db_cash_data_history_item

async def create_cash_data_history_item_if_not_exist(
    db: AsyncSession,
    cash_data_history_item: schemas.CashDataHistoryItemCreate,
    cash_data_history_id: Optional[int] = None
):
    if cash_data_history_id is None:
        existing_record = None
    else:
        query = select(models.CashDataHistoryItem).filter(
            models.CashDataHistoryItem.name == cash_data_history_item.name,
            models.CashDataHistoryItem.amount == cash_data_history_item.amount,
            models.CashDataHistoryItem.beginningTime == cash_data_history_item.beginningTime,
            models.CashDataHistoryItem.cash_data_history_id == cash_data_history_id
        )
        result = await db.execute(query)
        existing_record = result.scalars().first()

    if existing_record is None:
        return await create_cash_data_history_item(db, cash_data_history_item, cash_data_history_id)
    else:
        logger.debug(f'cash data history item already exist: {existing_record}')
        return existing_record

async def create_monetary_fund_data_history_item(
    db: AsyncSession,
    monetary_fund_data_history_item: schemas.MonetaryFundDataHistoryItemCreate,
    monetary_fund_data_history_id: Optional[int] = None
):
    create = False
    if monetary_fund_data_history_id is None:
        create = True
    else:
        query = select(models.MonetaryFundDataHistory).filter(models.MonetaryFundDataHistory.id == monetary_fund_data_history_id)
        result = await db.execute(query)
        if result.scalars().first() is None:
            create = True

    if create:
        history = await create_monetary_fund_data_history(db, schemas.MonetaryFundDataHistoryCreate())
        monetary_fund_data_history_id = history.id

    db_monetary_fund_data_history_item = models.MonetaryFundDataHistoryItem(**monetary_fund_data_history_item.model_dump())
    db_monetary_fund_data_history_item.monetary_fund_data_history_id = monetary_fund_data_history_id
    db.add(db_monetary_fund_data_history_item)
    await db.commit()
    await db.refresh(db_monetary_fund_data_history_item)
    return db_monetary_fund_data_history_item

async def create_monetary_fund_data_history_item_if_not_exist(
    db: AsyncSession,
    monetary_fund_data_history_item: schemas.MonetaryFundDataHistoryItemCreate,
    monetary_fund_data_history_id: Optional[int] = None
):
    if monetary_fund_data_history_id is None:
        existing_record = None
    else:
        query = select(models.MonetaryFundDataHistoryItem).filter(
            models.MonetaryFundDataHistoryItem.name == monetary_fund_data_history_item.name,
            models.MonetaryFundDataHistoryItem.beginningAmount == monetary_fund_data_history_item.beginningAmount,
            models.MonetaryFundDataHistoryItem.beginningTime == monetary_fund_data_history_item.beginningTime,
            models.MonetaryFundDataHistoryItem.beginningShares == monetary_fund_data_history_item.beginningShares,
            models.MonetaryFundDataHistoryItem.currentAmount == monetary_fund_data_history_item.currentAmount,
            models.MonetaryFundDataHistoryItem.currentTime == monetary_fund_data_history_item.currentTime,
            models.MonetaryFundDataHistoryItem.currentShares == monetary_fund_data_history_item.currentShares,
            models.MonetaryFundDataHistoryItem.currency == monetary_fund_data_history_item.currency,
            models.MonetaryFundDataHistoryItem.currencyRate == monetary_fund_data_history_item.currencyRate,
            models.MonetaryFundDataHistoryItem.beginningCurrencyRate == monetary_fund_data_history_item.beginningCurrencyRate,
            models.MonetaryFundDataHistoryItem.fastRedemption == monetary_fund_data_history_item.fastRedemption,
            models.MonetaryFundDataHistoryItem.holding == monetary_fund_data_history_item.holding,
            models.MonetaryFundDataHistoryItem.monetary_fund_data_history_id == monetary_fund_data_history_id
        )
        result = await db.execute(query)
        existing_record = result.scalars().first()

    if existing_record is None:
        return await create_monetary_fund_data_history_item(db, monetary_fund_data_history_item, monetary_fund_data_history_id)
    else:
        logger.debug(f'monetary fund data history item already exist: {existing_record}')
        return existing_record

async def create_fixed_deposit_data_history_item(
    db: AsyncSession,
    fixed_deposit_data_history_item: schemas.FixedDepositDataHistoryItemCreate,
    fixed_deposit_data_history_id: Optional[int] = None
):
    create = False
    if fixed_deposit_data_history_id is None:
        create = True
    else:
        query = select(models.FixedDepositDataHistory).filter(models.FixedDepositDataHistory.id == fixed_deposit_data_history_id)
        result = await db.execute(query)
        if result.scalars().first() is None:
            create = True

    if create:
        history = await create_fixed_deposit_data_history(db, schemas.FixedDepositDataHistoryCreate())
        fixed_deposit_data_history_id = history.id

    db_fixed_deposit_data_history_item = models.FixedDepositDataHistoryItem(**fixed_deposit_data_history_item.model_dump())
    db_fixed_deposit_data_history_item.fixed_deposit_data_history_id = fixed_deposit_data_history_id
    db.add(db_fixed_deposit_data_history_item)
    await db.commit()
    await db.refresh(db_fixed_deposit_data_history_item)
    return db_fixed_deposit_data_history_item

async def create_fixed_deposit_data_history_item_if_not_exist(
    db: AsyncSession,
    fixed_deposit_data_history_item: schemas.FixedDepositDataHistoryItemCreate,
    fixed_deposit_data_history_id: Optional[int] = None
):
    if fixed_deposit_data_history_id is None:
        existing_record = None
    else:
        query = select(models.FixedDepositDataHistoryItem).filter(
            models.FixedDepositDataHistoryItem.name == fixed_deposit_data_history_item.name,
            models.FixedDepositDataHistoryItem.beginningAmount == fixed_deposit_data_history_item.beginningAmount,
            models.FixedDepositDataHistoryItem.beginningTime == fixed_deposit_data_history_item.beginningTime,
            models.FixedDepositDataHistoryItem.rate == fixed_deposit_data_history_item.rate,
            models.FixedDepositDataHistoryItem.maturity == fixed_deposit_data_history_item.maturity,
            models.FixedDepositDataHistoryItem.fixed_deposit_data_history_id == fixed_deposit_data_history_id
        )
        result = await db.execute(query)
        existing_record = result.scalars().first()

    if existing_record is None:
        return await create_fixed_deposit_data_history_item(db, fixed_deposit_data_history_item, fixed_deposit_data_history_id)
    else:
        logger.debug(f'fixed deposit data history item already exist: {existing_record}')
        return existing_record

async def create_fund_data_history_item(
    db: AsyncSession,
    fund_data_history_item: schemas.FundDataHistoryItemCreate,
    fund_data_history_id: Optional[int] = None
):
    create = False
    if fund_data_history_id is None:
        create = True
    else:
        query = select(models.FundDataHistory).filter(models.FundDataHistory.id == fund_data_history_id)
        result = await db.execute(query)
        if result.scalars().first() is None:
            create = True

    if create:
        history = await create_fund_data_history(db, schemas.FundDataHistoryCreate())
        fund_data_history_id = history.id

    db_fund_data_history_item = models.FundDataHistoryItem(**fund_data_history_item.model_dump())
    db_fund_data_history_item.fund_data_history_id = fund_data_history_id
    db.add(db_fund_data_history_item)
    await db.commit()
    await db.refresh(db_fund_data_history_item)
    return db_fund_data_history_item

async def create_fund_data_history_item_if_not_exist(
    db: AsyncSession,
    fund_data_history_item: schemas.FundDataHistoryItemCreate,
    fund_data_history_id: Optional[int] = None
):
    if fund_data_history_id is None:
        existing_record = None
    else:
        query = select(models.FundDataHistoryItem).filter(
            models.FundDataHistoryItem.name == fund_data_history_item.name,
            models.FundDataHistoryItem.symbol == fund_data_history_item.symbol,
            models.FundDataHistoryItem.currentNetValue == fund_data_history_item.currentNetValue,
            models.FundDataHistoryItem.currentShares == fund_data_history_item.currentShares,
            models.FundDataHistoryItem.currentTime == fund_data_history_item.currentTime,
            models.FundDataHistoryItem.holding == fund_data_history_item.holding,
            models.FundDataHistoryItem.lockupPeriod == fund_data_history_item.lockupPeriod,
            models.FundDataHistoryItem.dividendRatio == fund_data_history_item.dividendRatio,
            models.FundDataHistoryItem.fund_data_history_id == fund_data_history_id
        )
        result = await db.execute(query)
        existing_record = result.scalars().first()

    if existing_record is None:
        return await create_fund_data_history_item(db, fund_data_history_item, fund_data_history_id)
    else:
        logger.debug(f'fund data history item already exist: {existing_record}')
        return existing_record

# ********** drop table **********

async def drop_all_tables(db: AsyncSession):
    await db.execute(text('DELETE FROM cash_data_history_item'))
    await db.execute(text('DELETE FROM cash_data_history'))
    await db.execute(text('DELETE FROM monetary_fund_data_history_item'))
    await db.execute(text('DELETE FROM monetary_fund_data_history'))
    await db.execute(text('DELETE FROM fixed_deposit_data_history_item'))
    await db.execute(text('DELETE FROM fixed_deposit_data_history'))
    await db.execute(text('DELETE FROM fund_data_history_item'))
    await db.execute(text('DELETE FROM fund_data_history'))
    await db.commit()

# ********** create from json **********

async def create_table_from_json(
    db: AsyncSession,
    json_data: Dict[str, Any]
):
    await drop_all_tables(db)

    create_history_func = {
        'cashData': create_cash_data_history,
        'monetaryFundData': create_monetary_fund_data_history,
        'fixedDepositData': create_fixed_deposit_data_history,
        'fundData': create_fund_data_history
    }
    create_item_func = {
        'cashData': create_cash_data_history_item_if_not_exist,
        'monetaryFundData': create_monetary_fund_data_history_item_if_not_exist,
        'fixedDepositData': create_fixed_deposit_data_history_item_if_not_exist,
        'fundData': create_fund_data_history_item_if_not_exist
    }
    history_schema = {
        'cashData': schemas.CashDataHistoryCreate,
        'monetaryFundData': schemas.MonetaryFundDataHistoryCreate,
        'fixedDepositData': schemas.FixedDepositDataHistoryCreate,
        'fundData': schemas.FundDataHistoryCreate
    }
    item_schema = {
        'cashData': schemas.CashDataHistoryItemCreate,
        'monetaryFundData': schemas.MonetaryFundDataHistoryItemCreate,
        'fixedDepositData': schemas.FixedDepositDataHistoryItemCreate,
        'fundData': schemas.FundDataHistoryItemCreate
    }


    for table_name in json_data.keys():
        table_data = json_data[table_name]
        logger.debug(f'Table name: {table_name}')
        for item in table_data:
            history = item['history']
            created = await create_history_func[table_name](db, history_schema[table_name]())
            history_id = created.id
            logger.debug(f'history id: {history_id}')

            for his in history:
                try:
                    await create_item_func[table_name](db, item_schema[table_name](**his), history_id)
                except Exception as e:
                    logger.error(table_name)
                    logger.error(his)
                    raise e
