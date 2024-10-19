import asyncio
from typing import Callable, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from libs.utils import trans_str_date_to_next_n_trade_date, trans_date_to_str

def run_async_task(func, *args):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(func(*args))

async def async_add_data_after_n_days_to_db(func: Callable, db: AsyncSession, dates: List[str], n: int):
    dates = [trans_str_date_to_next_n_trade_date(date, n) for date in dates]
    dates = [date for date in dates if date < datetime.now().date()]
    dates = [trans_date_to_str(date) for date in dates]
    await func(db, dates)

def add_data_after_n_days_to_db(func: Callable, db: AsyncSession, dates: List[str], n: int):
    run_async_task(async_add_data_after_n_days_to_db, func, db, dates, n)