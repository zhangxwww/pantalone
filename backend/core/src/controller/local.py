import json
import base64
from datetime import datetime

from loguru import logger

import sql_app.crud as crud
import sql_app.schemas as schemas


async def save_base64_data(db, data):
    content = base64.b64decode(data)
    json_data = json.loads(content.decode('utf-8'))
    await crud.create_table_from_json(db, json_data)

async def _get_cash_data_from_db(db):
    cash_data = []
    all_data = await crud.get_all_cash_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = await crud.get_cash_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'amount': his.amount,
                'beginningTime': his.beginningTime
            }
            history_list.append(h)
        cash_data.append({
            'id': history_id,
            'history': history_list
        })
    return cash_data

async def _get_monetary_fund_data_from_db(db):
    monetary_data = []
    all_data = await crud.get_all_monetary_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = await crud.get_monetary_fund_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'beginningAmount': his.beginningAmount,
                'beginningTime': his.beginningTime,
                'beginningShares': his.beginningShares,
                'currentAmount': his.currentAmount,
                'currentTime': his.currentTime,
                'currentShares': his.currentShares,
                'currency': his.currency,
                'currencyRate': his.currencyRate,
                'beginningCurrencyRate': his.beginningCurrencyRate,
                'fastRedemption': his.fastRedemption,
                'holding': his.holding
            }
            history_list.append(h)
        monetary_data.append({
            'id': history_id,
            'history': history_list
        })
    return monetary_data

async def _get_fixed_deposit_data_from_db(db):
    fixed_deposit_data = []
    all_data = await crud.get_all_fixed_deposit_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = await crud.get_fixed_deposit_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'beginningAmount': his.beginningAmount,
                'beginningTime': his.beginningTime,
                'rate': his.rate,
                'maturity': his.maturity
            }
            history_list.append(h)
        fixed_deposit_data.append({
            'id': history_id,
            'history': history_list
        })
    return fixed_deposit_data

async def _get_fund_data_from_db(db):
    fund_data = []
    all_data = await crud.get_all_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = await crud.get_fund_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'symbol': his.symbol,
                'currentNetValue': his.currentNetValue,
                'currentShares': his.currentShares,
                'currentTime': his.currentTime,
                'holding': his.holding,
                'lockupPeriod': his.lockupPeriod,
                'dividendRatio': his.dividendRatio
            }
            history_list.append(h)
        fund_data.append({
            'id': history_id,
            'history': history_list
        })
    return fund_data

async def get_data_from_db(db):
    return {
        'cashData': await _get_cash_data_from_db(db),
        'monetaryFundData': await _get_monetary_fund_data_from_db(db),
        'fixedDepositData': await _get_fixed_deposit_data_from_db(db),
        'fundData': await _get_fund_data_from_db(db)
    }

async def add_cash_history(db, data):
    item = schemas.CashDataHistoryItemCreate(**data.content.model_dump(), beginningTime=datetime.now().date())
    await crud.create_cash_data_history_item_if_not_exist(db, item, data.id)

async def add_monetary_fund_history(db, data):
    content = data.content.model_dump()

    logger.debug(content)

    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    content['currentTime'] = datetime.now().date()
    content['beginningShares'] = content['beginningAmount']
    item = schemas.MonetaryFundDataHistoryItemCreate(**content)
    await crud.create_monetary_fund_data_history_item_if_not_exist(db, item, data.id)

async def add_fixed_deposit_history(db, data):
    content = data.content.model_dump()
    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    item = schemas.FixedDepositDataHistoryItemCreate(**content)
    await crud.create_fixed_deposit_data_history_item_if_not_exist(db, item, data.id)

async def add_fund_history(db, data):
    content = data.content.model_dump()
    content['currentTime'] = datetime.now().date()
    item = schemas.FundDataHistoryItemCreate(**content)
    await crud.create_fund_data_history_item_if_not_exist(db, item, data.id)
