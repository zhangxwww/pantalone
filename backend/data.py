import json
import base64
from datetime import datetime

from chinese_calendar import is_workday

from spider import get_china_bond_yield
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
