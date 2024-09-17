import os
from datetime import datetime, timedelta

from chinese_calendar import is_workday


def get_log_file_path():
    log_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir



def _is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6


def trans_str_date_to_trade_date(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    now = datetime.now()
    if date > now.date():
        date = now.date()
        if now.hour < 18:
            date = date - timedelta(days=1)
    while not _is_trade_day(date):
        date = date - timedelta(days=1)
    return date