from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sql_app import models, schemas
from libs.decorators.cache import CacheWithExpiration
from ._decorators import _retry_when_db_locked


cache = CacheWithExpiration()

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

@cache(expiration_time=3600)
async def get_market_data(
    db: AsyncSession,
    code: str
):
    query = select(models.MarketData).filter(models.MarketData.code == code).order_by(models.MarketData.date)
    results = await db.execute(query)
    return results.scalars().all()

async def get_unique_market_code(
    db: AsyncSession
):
    query = select(models.MarketData.code).distinct()
    results = await db.execute(query)
    return results.scalars().all()
