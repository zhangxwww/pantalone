from typing import List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


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
