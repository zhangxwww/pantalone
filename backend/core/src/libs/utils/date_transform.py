import datetime

from chinese_calendar import is_workday


def _is_trade_day(date: datetime.date) -> bool:
    return is_workday(date) and date.isoweekday() < 6

def _find_latest_trade_day(date: datetime.date) -> datetime.date:
    while not _is_trade_day(date):
        date = date - datetime.timedelta(days=1)
    return date

def trans_date_to_trade_date(date: datetime.date) -> datetime.date:
    now = datetime.datetime.now()
    if date > now.date():
        date = now.date()
    if date == now.date() and now.hour < 18:
        date = date - datetime.timedelta(days=1)
    date = _find_latest_trade_day(date)
    return date

def trans_str_date_to_trade_date(date: str) -> datetime.date:
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return trans_date_to_trade_date(date)

def trans_str_date_to_next_n_trade_date(date: str, n: int) -> datetime.date:
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    date = date + datetime.timedelta(days=n)
    date = _find_latest_trade_day(date)
    return date

def trans_date_to_str(date: datetime.date) -> str:
    return date.strftime('%Y-%m-%d')

def get_one_quarter_before(year: int, quarter: int) -> tuple[int, int]:
    if quarter > 1:
        return year, quarter - 1
    else:
        return year - 1, 4

def get_dates_between_str(start_date: str, end_date: str) -> list[datetime.datetime]:
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    dates = []

    current_date_obj = start_date_obj
    while current_date_obj <= end_date_obj:
        dates.append(current_date_obj)
        current_date_obj += datetime.timedelta(days=1)

    return dates
