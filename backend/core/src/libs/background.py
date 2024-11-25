import asyncio
from typing import Callable, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from libs.utils.date_transform import trans_str_date_to_next_n_trade_date, trans_date_to_str
from libs.utils.asyncio import run_async_task


async def async_add_data_after_n_days_to_db(func: Callable, db: AsyncSession, dates: List[str], n: int):
    dates = [trans_str_date_to_next_n_trade_date(date, n) for date in dates]
    dates = [date for date in dates if date < datetime.now().date()]
    dates = [trans_date_to_str(date) for date in dates]
    try:
        await func(db, dates)
    except asyncio.CancelledError:
        logger.warning(f"Task add_data_after_n_days_to_db {func.__name__} has been cancelled.")

def add_data_after_n_days_to_db(func: Callable, db: AsyncSession, dates: List[str], n: int):
    run_async_task(async_add_data_after_n_days_to_db, func, db, dates, n)
