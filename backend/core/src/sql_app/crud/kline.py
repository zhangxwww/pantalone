from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sql_app import models, schemas
from libs.decorators.cache import CacheWithExpiration
from libs.decorators.return_type import return_copy_async
from ._decorators import _retry_when_db_locked


cache = CacheWithExpiration()

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

@cache(expiration_time=3600)
@return_copy_async
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

@cache(expiration_time=3600)
async def get_daily_kline_data_by_code(
    db: AsyncSession,
    code: str
):
    query = select(models.KLineData).where(
        models.KLineData.code == code,
        models.KLineData.period == 'daily'
    ).order_by(models.KLineData.date)
    results = await db.execute(query)
    return results.scalars().all()

async def get_unique_kline_code(
    db: AsyncSession
):
    query = select(models.KLineData.code).distinct()
    results = await db.execute(query)
    return results.scalars().all()