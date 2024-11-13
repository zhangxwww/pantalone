from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


# ********** stock/bond info data **********

@_retry_when_db_locked(retry_times=3)
async def create_stock_info_data_if_not_exists(
    db: AsyncSession,
    data: schemas.StockInfoDataCreate
):
    query = select(models.StockInfoData).filter(models.StockInfoData.code == data.code)
    result = await db.execute(query)
    existing_record = result.scalars().first()

    if existing_record is None:
        db_stock_info_data = models.StockInfoData(**data.model_dump())
        db.add(db_stock_info_data)
        await db.commit()
        await db.refresh(db_stock_info_data)
        return db_stock_info_data
    else:
        return existing_record


@_retry_when_db_locked(retry_times=3)
async def create_stock_info_data_from_list(
    db: AsyncSession,
    data: list[dict]
):
    for d in data:
        item = schemas.StockInfoDataCreate(**d)
        await create_stock_info_data_if_not_exists(db, item)


async def get_stock_info_data(
    db: AsyncSession,
    code: str
):
    query = select(models.StockInfoData).filter(models.StockInfoData.code == code)
    result = await db.execute(query)
    return result.scalars().one_or_none()


@_retry_when_db_locked(retry_times=3)
async def create_bond_info_data_if_not_exists(
    db: AsyncSession,
    data: schemas.BondInfoDataCreate
):
    query = select(models.BondInfoData).filter(models.BondInfoData.code == data.code)
    result = await db.execute(query)
    existing_record = result.scalars().first()

    if existing_record is None:
        db_bond_info_data = models.BondInfoData(**data.model_dump())
        db.add(db_bond_info_data)
        await db.commit()
        await db.refresh(db_bond_info_data)
        return db_bond_info_data
    else:
        return existing_record


@_retry_when_db_locked(retry_times=3)
async def create_bond_info_data_from_list(
    db: AsyncSession,
    data: list[dict]
):
    for d in data:
        item = schemas.BondInfoDataCreate(**d)
        await create_bond_info_data_if_not_exists(db, item)


async def get_bond_info_data(
    db: AsyncSession,
    code: str
):
    query = select(models.BondInfoData).filter(models.BondInfoData.code == code)
    result = await db.execute(query)
    return result.scalars().one_or_none()