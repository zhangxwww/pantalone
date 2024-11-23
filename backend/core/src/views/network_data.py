from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

import api_model
import controller.network as network_controller
import controller.calculation as calculation_controller
from db import get_db
from libs.decorators.timeit import timeit
from libs.decorators.log import log_request, log_response
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
        background_tasks.add_task(add_data_after_n_days_to_db, network_controller.get_china_bond_yield_data, db, data.dates, n_days)
    return {'yields': await network_controller.get_china_bond_yield_data(db, data.dates)}


@router.post('/lpr')
@log_request
@log_response
@timeit
async def get_lpr(data: api_model.LPRDateData, db: AsyncSession = Depends(get_db)):
    return {'lpr': await network_controller.get_lpr_data(db, data.dates)}


@router.post('/index-close')
@log_request
@log_response
@timeit
async def get_index_close(data: api_model.IndexCloseDateData, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    for n_days in [1, 2, 3]:
        background_tasks.add_task(add_data_after_n_days_to_db, network_controller.get_index_close_data, db, data.dates, n_days)
    return {'close': await network_controller.get_index_close_data(db, data.dates)}


@router.post('/fund-name')
@log_request
@log_response
@timeit
async def get_fund_name(data: api_model.QueryFundNameData, db: AsyncSession = Depends(get_db)):
    return {'fund_name': await network_controller.get_fund_name(db, data.symbol)}


@router.post('/refresh')
@log_request
@log_response
@timeit
async def get_refresh_data(data: api_model.RefreshFundNetValueData):
    return {'refresh': await network_controller.get_refreshed_fund_net_value(data.symbols)}


@router.post('/holding')
@log_request
@timeit
async def get_holding_data(data: api_model.GetFundHoldingData, db: AsyncSession = Depends(get_db)):
    return {'holding': await network_controller.get_fund_holding_data(db, data.symbols)}


@router.post('/relevance')
@timeit
async def get_relevance_data(data: api_model.GetFundHoldingRelevanceData):
    return {'relevance': await network_controller.get_fund_holding_relevance_data(data.holding)}


@router.post('/kline')
@log_request
@timeit
async def get_kline_data(data: api_model.GetKLineData, db: AsyncSession = Depends(get_db)):
    return {'kline': await network_controller.get_kline_data(db, data)}


@router.post('/market')
@log_request
@timeit
async def get_market_data(data: api_model.GetMarketData, db: AsyncSession = Depends(get_db)):
    return {'market': await network_controller.get_market_data(db, data.instrument)}


@router.get('/playground/ucp-list')
@timeit
async def get_ucp_list(db: AsyncSession = Depends(get_db)):
    return {'ucp_list': await calculation_controller.get_ucp_list(db)}


@router.post('/playground/ucp-query')
@log_request
@timeit
async def get_ucp_query_result(data: api_model.GetUCPQueryResultRequestData, db: AsyncSession = Depends(get_db)):
    return {'ucp_query_result': await calculation_controller.get_ucp_query_result(db, data.ucp, data.interval, data.func, data.start_date, data.end_date)}


@router.post('/latest-currency-rate')
@log_request
@log_response
@timeit
async def get_latest_currency_rate(data: api_model.LatestCurrencyRateData, db: AsyncSession = Depends(get_db)):
    return {'rate': await network_controller.get_latest_currency_rate(db, data.symbol)}


@router.post('/price-percentile')
@log_request
@timeit
async def get_price_percentile(data: api_model.PercentileRequestData, db: AsyncSession = Depends(get_db)):
    return {'data': await calculation_controller.get_percentile(db, data)}


@router.post('/expected-return')
@log_request
@timeit
async def get_expected_return(data: api_model.ExpectedReturnRequestData, db: AsyncSession = Depends(get_db)):
    return {'data': await calculation_controller.get_expected_return(db, data)}


@router.post('/stock-bond-info')
@log_request
@timeit
async def get_stock_bond_info(data: api_model.GetStockBondInfoRequestData, db: AsyncSession = Depends(get_db)):
    return {'data': await network_controller.get_stock_bond_info(db, data.stocks, data.bonds)}
