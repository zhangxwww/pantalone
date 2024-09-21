import os
from datetime import datetime, timedelta
import functools
import time

from loguru import logger
from chinese_calendar import is_workday


def timeit(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {elapsed_time:.8f} seconds")
        return result
    return wrapper


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