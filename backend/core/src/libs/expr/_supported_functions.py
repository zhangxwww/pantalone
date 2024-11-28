import pandas as pd


def shift(data: pd.Series, n: int) -> pd.Series:
    return data.shift(n)

def diff(data: pd.Series, n: int) -> pd.Series:
    return data.diff(n)

def rmin(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).min()

def rmax(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).max()

def rmean(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).mean()

def rstd(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).std()

def rsum(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).sum()

def rprod(data: pd.Series, n: int) -> pd.Series:
    return data.rolling(window=n).prod()

def rcorr(data1: pd.Series, data2: pd.Series, n: int) -> pd.Series:
    return data1.rolling(window=n).corr(data2)

def csum(data: pd.Series) -> pd.Series:
    return data.cumsum()

def cprod(data: pd.Series) -> pd.Series:
    return data.cumprod()
