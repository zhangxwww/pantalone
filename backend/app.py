import os

from scipy.stats import chi2, t, norm
from fastapi import FastAPI, staticfiles, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from loguru import logger

import operation
import api_model
from sql_app import models
from sql_app.database import SessionLocal, engine
from utils import get_log_file_path, timeit
from background import add_data_after_n_days_to_db


logger.add(
    os.path.join(get_log_file_path(), '{time}.log'),
    level='DEBUG',
    rotation='1 day',
    retention='1 week',
    compression='zip')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/CN1YR')
@timeit
async def get_CN1YR(
    data: api_model.CN1YRDateData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.debug(data.dates)
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_CN1YR_data, db, data.dates, n_days)
    return {'yields': operation.get_china_bond_yield_data(db, data.dates)}


@app.post('/api/lpr')
@timeit
async def get_lpr(data: api_model.LPRDateData, db: Session = Depends(get_db)):
    logger.debug(data.dates)
    return {'lpr': operation.get_lpr_data(db, data.dates)}


@app.post('/api/index-close')
@timeit
async def get_sh_close(data: api_model.IndexCloseDateData, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.debug(data.dates)
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_index_close_data, db, data.dates, n_days)
    return {'close': operation.get_index_close_data(db, data.dates)}


@app.post('/api/upload')
@timeit
async def upload(file: api_model.UploadData, db: Session = Depends(get_db)):
    operation.save_base64_data(db, file.file)
    return {'success': True}


@app.post('/api/data/cash')
@timeit
async def add_cash(data: api_model.AddCashHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_cash_history(db, data)
    return {'success': True}


@app.post('/api/data/monetary-fund')
@timeit
async def add_monetary(data: api_model.AddMonetaryFundHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_monetary_fund_history(db, data)
    return {'success': True}


@app.post('/api/data/fixed-deposit')
@timeit
async def add_fixed(data: api_model.AddFixedDepositHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_fixed_deposit_history(db, data)
    return {'success': True}


@app.post('/api/data/fund')
@timeit
async def add_fund(data: api_model.AddFundHistoryData, db: Session = Depends(get_db)):
    logger.debug(data)
    operation.add_fund_history(db, data)
    return {'success': True}


@app.get('/api/data')
@timeit
async def get_data(db: Session = Depends(get_db)):
    return operation.get_data_from_db(db)


@app.get('/api/statistics/chi2/interval')
@timeit
async def get_chi2_interval(p: float, df: int):
    logger.debug(f'chi2 p: {p}, df: {df}')
    # https://blog.csdn.net/u012958850/article/details/116565996
    lower, upper = chi2.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@app.get('/api/statistics/t/interval')
@timeit
async def get_t_interval(p: float, df: int):
    logger.debug(f't: p: {p}, df: {df}')
    lower, upper = t.interval(p, df)
    return {
        'lower': lower,
        'upper': upper
    }


@app.get('/api/statistics/normal/interval')
@timeit
async def get_normal_interval(p: float):
    logger.debug(f'normal: p: {p}')
    lower, upper = norm.interval(p)
    return {
        'lower': lower,
        'upper': upper
    }


app.mount('/', staticfiles.StaticFiles(directory='../frontend/dist/', html=True), name='static')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=9876, reload=True)