from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

import api_model
import controller.local as local_controller
from libs.decorators.timeit import timeit
from libs.decorators.log import log_request
from db import get_db


router = APIRouter(prefix='/data', tags=['data'])

@router.post('/cash')
@log_request
@timeit
async def add_cash(data: api_model.AddCashHistoryData, db: AsyncSession = Depends(get_db)):
    logger.debug(data)
    await local_controller.add_cash_history(db, data)
    return {'success': True}


@router.post('/monetary-fund')
@log_request
@timeit
async def add_monetary(data: api_model.AddMonetaryFundHistoryData, db: AsyncSession = Depends(get_db)):
    logger.debug(data)
    await local_controller.add_monetary_fund_history(db, data)
    return {'success': True}


@router.post('/fixed-deposit')
@log_request
@timeit
async def add_fixed(data: api_model.AddFixedDepositHistoryData, db: AsyncSession = Depends(get_db)):
    logger.debug(data)
    await local_controller.add_fixed_deposit_history(db, data)
    return {'success': True}


@router.post('/fund')
@log_request
@timeit
async def add_fund(data: api_model.AddFundHistoryData, db: AsyncSession = Depends(get_db)):
    logger.debug(data)
    await local_controller.add_fund_history(db, data)
    return {'success': True}


@router.get('')
@log_request
@timeit
async def get_data(db: AsyncSession = Depends(get_db)):
    return await local_controller.get_data_from_db(db)
