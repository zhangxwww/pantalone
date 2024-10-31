from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from libs.utils.decorator import timeit, log_request, log_response
import api_model
import libs.operation as operation
from db import get_db
from libs.background import add_data_after_n_days_to_db


router = APIRouter(tags=['network'])

@router.post('/CN1YR')
@log_request
@log_response
@timeit
async def get_CN1YR(
    data: api_model.CN1YRDateData,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_china_bond_yield_data, db, data.dates, n_days)
    return {'yields': await operation.get_china_bond_yield_data(db, data.dates)}


@router.post('/lpr')
@log_request
@log_response
@timeit
async def get_lpr(data: api_model.LPRDateData, db: AsyncSession = Depends(get_db)):
    return {'lpr': await operation.get_lpr_data(db, data.dates)}


@router.post('/index-close')
@log_request
@log_response
@timeit
async def get_index_close(data: api_model.IndexCloseDateData, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, operation.get_index_close_data, db, data.dates, n_days)
    return {'close': await operation.get_index_close_data(db, data.dates)}


@router.post('/fund-name')
@log_request
@log_response
@timeit
async def get_fund_name(data: api_model.QueryFundNameData, db: AsyncSession = Depends(get_db)):
    return {'fund_name': await operation.get_fund_name(db, data.symbol)}


@router.post('/refresh')
@log_request
@log_response
@timeit
async def get_refresh_data(data: api_model.RefreshFundNetValueData):
    return {'refresh': await operation.get_refreshed_fund_net_value(data.symbols)}


@router.post('/holding')
@log_request
@timeit
async def get_holding_data(data: api_model.GetFundHoldingData, db: AsyncSession = Depends(get_db)):
    return {'holding': await operation.get_fund_holding_data(db, data.symbols)}


@router.post('/relevance')
@timeit
async def get_relevance_data(data: api_model.GetFundHoldingRelevanceData):
    return {'relevance': await operation.get_fund_holding_relevance_data(data.holding)}


@router.post('/kline')
@log_request
@timeit
async def get_kline_data(data: api_model.GetKLineData, db: AsyncSession = Depends(get_db)):
    return {'kline': await operation.get_kline_data(db, data)}


@router.post('/market')
@log_request
@timeit
async def get_market_data(data: api_model.GetMarketData, db: AsyncSession = Depends(get_db)):
    return {'market': await operation.get_market_data(db, data.instrument)}


@router.post('/latest-currency-rate')
@log_request
@log_response
@timeit
async def get_latest_currency_rate(data: api_model.LatestCurrencyRateData, db: AsyncSession = Depends(get_db)):
    return {'rate': await operation.get_latest_currency_rate(db, data.symbol)}


@router.post('/price-percentile')
@log_request
@timeit
async def get_price_percentile(data: api_model.PercentileRequestData, db: AsyncSession = Depends(get_db)):
    return {'data': await operation.get_percentile(db, data)}


@router.post('/stock-bond-info')
@log_request
@timeit
async def get_stock_bond_info(data: api_model.GetStockBondInfoRequestData, db: AsyncSession = Depends(get_db)):
    return {'data': await operation.get_stock_bond_info(db, data.stocks, data.bonds)}