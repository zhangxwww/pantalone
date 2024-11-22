from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sql_app import models, schemas


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