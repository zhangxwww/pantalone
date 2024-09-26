from typing import Callable, List
from datetime import datetime

from sqlalchemy.orm import Session

from utils import trans_str_date_to_next_n_trade_date, trans_date_to_str


def add_data_after_n_days_to_db(func: Callable, db: Session, dates: List[str], n: int):
    dates = [trans_str_date_to_next_n_trade_date(date, n) for date in dates]
    dates = [date for date in dates if date < datetime.now().date()]
    dates = [trans_date_to_str(date) for date in dates]
    return func(db, dates)