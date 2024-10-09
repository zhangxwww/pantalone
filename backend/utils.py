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

def log_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Request: {func.__name__}")
        logger.info(f"Args: {args}")
        logger.info(f"Kwargs: {kwargs}")
        return await func(*args, **kwargs)
    return wrapper

def log_response(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        logger.info(f"Response: {func.__name__}")
        logger.info(f"Result: {result}")
        return result
    return wrapper


def get_log_file_path():
    log_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir



def _is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6


def _find_latest_trade_day(date):
    while not _is_trade_day(date):
        date = date - timedelta(days=1)
    return date


def trans_str_date_to_trade_date(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    now = datetime.now()
    if date > now.date():
        date = now.date()
    if date == now.date() and now.hour < 18:
        date = date - timedelta(days=1)
    date = _find_latest_trade_day(date)
    return date


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