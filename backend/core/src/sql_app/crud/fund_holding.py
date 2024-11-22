from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ._decorators import _retry_when_db_locked
from sql_app import models, schemas


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