import json
import base64
from datetime import datetime, timedelta

from chinese_calendar import is_workday
from loguru import logger

from spider import get_china_bond_yield
import sql_app.schemas as schemas
import sql_app.crud as crud


def _is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6


def get_china_bond_yield_data(db, dates):
    query_dates = []
    for date in dates:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        now = datetime.now()
        if date > now.date():
            date = now.date()
            if now.hour < 18:
                date = date - timedelta(days=1)
        while not _is_trade_day(date):
            date = date - timedelta(days=1)
        query_dates.append(date)

    logger.debug('Query dates: ')
    logger.debug(query_dates)

    db_data = crud.get_CN1YR_data(db, query_dates)

    db_data_list = [{'date': d.date, 'yield': d.yield_1yr} for d in db_data]

    logger.debug('DB data: ')
    logger.debug(db_data_list)

    not_found_dates = list(set(query_dates) - set(d.date for d in db_data))

    logger.debug('Not found dates: ')
    logger.debug(not_found_dates)

    not_found_dates_yield = []
    for date in not_found_dates:
        yield_1yr = get_china_bond_yield(date)
        item = schemas.CN1YRDataCreate(date=date, yield_1yr=yield_1yr)
        not_found_dates_yield.append(item)
    crud.create_CN1YR_data_from_list(db, not_found_dates_yield)

    spider_data = [{'date': d.date, 'yield': d.yield_1yr} for d in not_found_dates_yield]

    logger.debug('Spider data: ')
    logger.debug(spider_data)

    data = db_data_list + spider_data
    data = sorted(data, key=lambda x: x['date'])

    logger.debug('Final data: ')
    logger.debug(data)

    return data


def save_base64_data(db, data):
    content = base64.b64decode(data)
    json_data = json.loads(content.decode('utf-8'))
    crud.create_table_from_json(db, json_data)


def _get_cash_data_from_db(db):
    cash_data = []
    all_data = crud.get_all_cash_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_cash_data_history_item_by_history_id(db, history_id)

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

def _get_monetary_fund_data_from_db(db):
    monetary_data = []
    all_data = crud.get_all_monetary_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_monetary_fund_data_history_item_by_history_id(db, history_id)

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
                'fastRedemption': his.fastRedemption,
                'holding': his.holding
            }
            history_list.append(h)
        monetary_data.append({
            'id': history_id,
            'history': history_list
        })
    return monetary_data

def _get_fixed_deposit_data_from_db(db):
    fixed_deposit_data = []
    all_data = crud.get_all_fixed_deposit_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_fixed_deposit_data_history_item_by_history_id(db, history_id)

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

def _get_fund_data_from_db(db):
    fund_data = []
    all_data = crud.get_all_fund_data_history(db)
    for history in all_data:
        history_id = history.id
        history_data = crud.get_fund_data_history_item_by_history_id(db, history_id)

        history_list = []
        for his in history_data:
            h = {
                'name': his.name,
                'currentNetValue': his.currentNetValue,
                'currentShares': his.currentShares,
                'currentTime': his.currentTime,
                'holding': his.holding,
                'lockupPeriod': his.lockupPeriod
            }
            history_list.append(h)
        fund_data.append({
            'id': history_id,
            'history': history_list
        })
    return fund_data


def get_data_from_db(db):
    return {
        'cashData': _get_cash_data_from_db(db),
        'monetaryFundData': _get_monetary_fund_data_from_db(db),
        'fixedDepositData': _get_fixed_deposit_data_from_db(db),
        'fundData': _get_fund_data_from_db(db)
    }


def add_cash_history(db, data):
    item = schemas.CashDataHistoryItemCreate(**data.content.model_dump(), beginningTime=datetime.now().date())
    crud.create_cash_data_history_item(db, item, data.id)


def add_monetary_fund_history(db, data):
    content = data.content.model_dump()

    logger.debug(content)

    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    content['currentTime'] = datetime.now().date()
    content['beginningShares'] = content['beginningAmount']
    item = schemas.MonetaryFundDataHistoryItemCreate(**content)
    crud.create_monetary_fund_data_history_item(db, item, data.id)


def add_fixed_deposit_history(db, data):
    content = data.content.model_dump()
    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    item = schemas.FixedDepositDataHistoryItemCreate(**content)
    crud.create_fixed_deposit_data_history_item(db, item, data.id)


def add_fund_history(db, data):
    content = data.content.model_dump()
    content['currentTime'] = datetime.now().date()
    item = schemas.FundDataHistoryItemCreate(**content)
    crud.create_fund_data_history_item(db, item, data.id)