import json
import base64
from datetime import datetime

from chinese_calendar import is_workday
from loguru import logger

from spider import get_china_bond_yield
import sql_app.schemas as schemas
import sql_app.crud as crud


def is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6


def get_china_bond_bield_data(dates):
    data = []
    for date in dates:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        now = datetime.now()
        if date > now.date():
            date = now.date()
            if now.hour < 18:
                date = date.replace(day=date.day - 1)
        while not is_trade_day(date):
            date = date.replace(day=date.day - 1)
        data.append(get_china_bond_yield(date))
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
                'currentAmount': his.currentAmount,
                'currentTime': his.currentTime,
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
                'beginningAmount': his.beginningAmount,
                'beginningTime': his.beginningTime,
                'currentAmount': his.currentAmount,
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
    bg_time = content['beginningTime']
    content['beginningTime'] = datetime.strptime(bg_time, '%Y-%m-%d').date()
    content['currentTime'] = datetime.now().date()
    item = schemas.FundDataHistoryItemCreate(**content)
    crud.create_fund_data_history_item(db, item, data.id)