from fastapi import APIRouter, Depends, BackgroundTasks
from loguru import logger
from sqlalchemy.orm import Session

from utils import timeit
import api_model
import operation
from db import get_db
from background import add_data_after_n_days_to_db


router = APIRouter(tags=['network'])

@router.post('/CN1YR')
@timeit
async def get_CN1YR(
    data: api_model.CN1YRDateData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.debug(data.dates)
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_china_bond_yield_data, db, data.dates, n_days)
    return {'yields': operation.get_china_bond_yield_data(db, data.dates)}


@router.post('/lpr')
@timeit
async def get_lpr(data: api_model.LPRDateData, db: Session = Depends(get_db)):
    logger.debug(data.dates)
    return {'lpr': operation.get_lpr_data(db, data.dates)}


@router.post('/index-close')
@timeit
async def get_sh_close(data: api_model.IndexCloseDateData, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.debug(data.dates)
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_index_close_data, db, data.dates, n_days)
    return {'close': operation.get_index_close_data(db, data.dates)}


@router.post('/fund-name')
@timeit
async def get_fund_name(data: api_model.QueryFundNameData, db: Session = Depends(get_db)):
    logger.debug(data.symbol)
    return {'fund_name': operation.get_fund_name(db, data.symbol)}