from datetime import datetime

from chinese_calendar import is_workday

from spider import getChinaBondYield


def is_trade_day(date):
    return is_workday(date) and date.isoweekday() < 6


def getChinaBondYieldData(dates):
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
        data.append(getChinaBondYield(date))
    return data