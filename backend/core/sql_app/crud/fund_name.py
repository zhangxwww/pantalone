from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


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