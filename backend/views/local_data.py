from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from utils import timeit
import api_model
import operation
from db import get_db


router = APIRouter(prefix='/data', tags=['data'])

@router.post('/cash')
@timeit
async def add_cash(data: api_model.AddCashHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_cash_history(db, data)
    return {'success': True}


@router.post('/monetary-fund')
@timeit
async def add_monetary(data: api_model.AddMonetaryFundHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_monetary_fund_history(db, data)
    return {'success': True}


@router.post('/fixed-deposit')
@timeit
async def add_fixed(data: api_model.AddFixedDepositHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_fixed_deposit_history(db, data)
    return {'success': True}


@router.post('/fund')
@timeit
async def add_fund(data: api_model.AddFundHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_fund_history(db, data)
    return {'success': True}


@router.get('')
@timeit
async def get_data(db: Session = Depends(get_db)):
    return operation.get_data_from_db(db)
