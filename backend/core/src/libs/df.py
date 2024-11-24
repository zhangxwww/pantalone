import pandas as pd


def resample(daily_df, period):
    df = daily_df.copy()
    if period == 'daily':
        return df
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    sample = 'W' if period == 'weekly' else 'ME'
    agg_df = df.resample(sample).agg({
        'value': 'last'
    }).dropna()
    agg_df = agg_df.reset_index()
    agg_df['date'] = agg_df['date'].dt.date
    return agg_df

def cut_by_window(df, window, unit='year'):
    if window == -1:
        return df.copy()
    current_data = pd.Timestamp.now()
    if unit == 'year':
        start_date = current_data - pd.DateOffset(years=window)
    elif unit == 'month':
        start_date = current_data - pd.DateOffset(months=window)
    elif unit == 'day':
        start_date = current_data - pd.DateOffset(days=window)
    filtered = df[df['date'] >= start_date.date()]
    return filtered

def percentile(df):
    last_value = df['value'].iloc[-1]
    percentile = (df['value'] < last_value).sum() / df.shape[0] * 100
    return percentile
