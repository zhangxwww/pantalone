from typing import Optional, Dict, Any, List
from datetime import date
from functools import wraps
import asyncio
import random

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError
from loguru import logger

from . import models, schemas


def _retry_when_db_locked(retry_times: int = 3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    if 'database is locked' in str(e):
                        logger.warning(f'Error: {e}')
                        logger.warning(f'Retry {i + 1}/{retry_times}')
                        db = args[0]
                        await db.rollback()
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        raise e
        return wrapper
    return decorator


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


# ********** add CN1YR data **********

@_retry_when_db_locked(retry_times=3)
async def create_CN1YR_data(
    db: AsyncSession,
    data: schemas.CN1YRDataCreate
):
    db_CN1YR_data = models.ChinaBondYield(**data.model_dump())
    db.add(db_CN1YR_data)
    await db.commit()
    await db.refresh(db_CN1YR_data)
    return db_CN1YR_data


@_retry_when_db_locked(retry_times=3)
async def create_CN1YR_data_from_list(
    db: AsyncSession,
    data: List[schemas.CN1YRDataCreate]
):
    for item in data:
        await create_CN1YR_data(db, item)


# ********** get CN1YR data **********

async def get_CN1YR_data(
    db: AsyncSession,
    dates: List[date]
):
    query = select(models.ChinaBondYield).filter(models.ChinaBondYield.date.in_(dates))
    result = await db.execute(query)
    return result.scalars().all()


# ********** add lpr data **********

@_retry_when_db_locked(retry_times=3)
async def create_lpr_data(
    db: AsyncSession,
    data: schemas.LPRDataCreate
):
    db_lpr_data = models.LPR(**data.model_dump())
    db.add(db_lpr_data)
    await db.commit()
    await db.refresh(db_lpr_data)
    return db_lpr_data


@_retry_when_db_locked(retry_times=3)
async def create_lpr_data_from_list(
    db: AsyncSession,
    data: List[schemas.LPRDataCreate]
):
    for item in data:
        await create_lpr_data(db, item)


# ********** get lpr data **********

async def get_lpr_data(
    db: AsyncSession,
    dates: List[date]
):
    query = select(models.LPR).filter(models.LPR.date.in_(dates))
    result = await db.execute(query)
    return result.scalars().all()


# ********** save index close data **********

@_retry_when_db_locked(retry_times=3)
async def create_index_close_data(
    db: AsyncSession,
    data: schemas.IndexCloseDataCreate
):
    db_index_close_data = models.IndexClose(**data.model_dump())
    db.add(db_index_close_data)
    await db.commit()
    await db.refresh(db_index_close_data)
    return db_index_close_data


@_retry_when_db_locked(retry_times=3)
async def create_index_close_data_from_list(
    db: AsyncSession,
    data: List[schemas.IndexCloseDataCreate]
):
    for item in data:
        await create_index_close_data(db, item)

# ********** get index close data **********

async def get_index_close_data(
    db: AsyncSession,
    dates: List[date]
):
    query = select(models.IndexClose).filter(models.IndexClose.date.in_(dates))
    result = await db.execute(query)
    return result.scalars().all()


# ********** fund name data **********

async def get_fund_name(
    db: AsyncSession,
    symbol: str
):
    query = select(models.FundName).filter(models.FundName.symbol == symbol)
    result = await db.execute(query)
    return result.scalars().one_or_none()


@_retry_when_db_locked(retry_times=3)
async def create_fund_name(
    db: AsyncSession,
    data: schemas.FundNameDataCreate
):
    db_fund_name = models.FundName(**data.model_dump())
    db.add(db_fund_name)
    await db.commit()
    await db.refresh(db_fund_name)
    return db_fund_name


# ********** fund holding data **********

async def get_fund_holding_data(
    db: AsyncSession,
    year: int,
    quarter: int,
    fund_code: str,
    type_: str
):
    query = select(models.FundHolding).filter(
        models.FundHolding.year == year,
        models.FundHolding.quarter == quarter,
        models.FundHolding.fund_code == fund_code
    )
    if type_ != 'all':
        query = query.filter(models.FundHolding.type == type_)

    result = await db.execute(query)
    return result.scalars().all()


@_retry_when_db_locked(retry_times=3)
async def create_fund_holding_data(
    db: AsyncSession,
    data: schemas.FundHoldingDataCreate
):
    db_fund_holding_data = models.FundHolding(**data.model_dump())
    db.add(db_fund_holding_data)
    await db.commit()
    await db.refresh(db_fund_holding_data)
    return db_fund_holding_data


@_retry_when_db_locked(retry_times=3)
async def create_fund_holding_data_if_not_exist(
    db: AsyncSession,
    data: schemas.FundHoldingDataCreate
):
    query = select(models.FundHolding).filter(
        models.FundHolding.fund_code == data.fund_code,
        models.FundHolding.year == data.year,
        models.FundHolding.quarter == data.quarter,
        models.FundHolding.code == data.code,
        models.FundHolding.type == data.type
    )
    result = await db.execute(query)
    existing_record = result.scalars().first()

    if existing_record is None:
        return await create_fund_holding_data(db, data)
    else:
        return existing_record


# ********** holding not found in spider history **********

async def create_holding_not_found_in_spider_history_data(
    db: AsyncSession,
    data: schemas.HoldingNotFoundInSpiderHistoryCreate
):
    db_holding_not_found_in_spider_history = models.HoldingNotFoundInSpiderHistory(**data.model_dump())
    db.add(db_holding_not_found_in_spider_history)
    await db.commit()
    await db.refresh(db_holding_not_found_in_spider_history)
    return db_holding_not_found_in_spider_history


async def find_holding_not_found_in_spider_history_data(
    db: AsyncSession,
    code: str,
    year: int,
    quarter: int
):
    query = select(models.HoldingNotFoundInSpiderHistory).filter(
        models.HoldingNotFoundInSpiderHistory.code == code,
        models.HoldingNotFoundInSpiderHistory.year == year,
        models.HoldingNotFoundInSpiderHistory.quarter == quarter
    )
    result = await db.execute(query)
    return result.scalars().one_or_none()


# ********** kline data **********

@_retry_when_db_locked(retry_times=3)
async def create_kline_data(
    db: AsyncSession,
    data: schemas.KLineDataCreate
):
    db_kline_data = models.KLineData(**data.model_dump())
    db.add(db_kline_data)
    await db.commit()
    await db.refresh(db_kline_data)
    return db_kline_data


@_retry_when_db_locked(retry_times=3)
async def create_kline_data_from_list(
    db: AsyncSession,
    data: list[dict],
    code: str,
    period: str,
    market: str
):
    for d in data:
        item = schemas.KLineDataCreate(**d, code=code, period=period, market=market)
        item = models.KLineData(**item.model_dump())
        db.add(item)
    await db.commit()


async def get_kline_data(
    db: AsyncSession,
    code: str,
    period: str,
    market: str
):
    query = select(models.KLineData).where(
        models.KLineData.code == code,
        models.KLineData.period == period,
        models.KLineData.market == market
    ).order_by(models.KLineData.date)
    results = await db.execute(query)
    return results.scalars().all()


# ********** market data **********

@_retry_when_db_locked(retry_times=3)
async def create_market_data(
    db: AsyncSession,
    data: schemas.MarketDataCreate
):
    db_market_data = models.MarketData(**data.model_dump())
    db.add(db_market_data)
    await db.commit()
    await db.refresh(db_market_data)
    return db_market_data


@_retry_when_db_locked(retry_times=3)
async def create_market_data_from_list(
    db: AsyncSession,
    data: list[dict],
    code: str
):
    for d in data:
        item = schemas.MarketDataCreate(**d, code=code)
        item = models.MarketData(**item.model_dump())
        db.add(item)
    await db.commit()


async def get_market_data(
    db: AsyncSession,
    code: str
):
    query = select(models.MarketData).filter(models.MarketData.code == code).order_by(models.MarketData.date)
    results = await db.execute(query)
    return results.scalars().all()