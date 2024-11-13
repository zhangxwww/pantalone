from typing import List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


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