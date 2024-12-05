from datetime import datetime, timedelta

from chinese_calendar import is_workday


def _is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6

def _find_latest_trade_day(date):
    while not _is_trade_day(date):
        date = date - timedelta(days=1)
    return date

def trans_date_to_trade_date(date):
    now = datetime.now()
    if date > now.date():
        date = now.date()
    if date == now.date() and now.hour < 18:
        date = date - timedelta(days=1)
    date = _find_latest_trade_day(date)
    return date

def trans_str_date_to_trade_date(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    return trans_date_to_trade_date(date)

def trans_str_date_to_next_n_trade_date(date, n):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    date = date + timedelta(days=n)
    date = _find_latest_trade_day(date)
    return date

def trans_date_to_str(date):
    return date.strftime('%Y-%m-%d')

def get_one_quarter_before(year, quarter):
    if quarter > 1:
        return year, quarter - 1
    else:
        return year - 1, 4

def get_dates_between_str(start_date: str, end_date: str):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    dates = []

    current_date_obj = start_date_obj
    while current_date_obj <= end_date_obj:
        dates.append(current_date_obj)
        current_date_obj += timedelta(days=1)

    return dates
