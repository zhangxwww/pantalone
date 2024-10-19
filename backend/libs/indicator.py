import pandas as pd


def list_dict_to_dataframe(data):
    return pd.DataFrame(data)


def dataframe_to_list_dict(df):
    return df.to_dict(orient='records')


def boll(df, window, width):
    rolling = df['close'].rolling(window=window)
    sma = rolling.mean()
    std = rolling.std()
    upper = sma + std * width
    lower = sma - std * width
    df['mid'] = sma
    df['upper'] = upper
    df['lower'] = lower
    return df
