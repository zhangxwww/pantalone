from typing import List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


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