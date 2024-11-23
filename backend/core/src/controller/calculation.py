import math
import traceback
from datetime import datetime
from joblib import Parallel, delayed

from loguru import logger

import numpy as np
import pandas as pd

import api_model
import sql_app.crud as crud
from libs.protocol.ucp import UCP
from libs.expr.expr import Executor, Preprocessor
from libs.expr.supported_operations import SUPPORTED_OPERATIONS
from libs.math.estimation import estimate_normal_distribution
from libs.math.geometric_random_walk import exp_geometric_random_walk, std_geometric_random_walk
from libs.math.interval import normal_interval
from libs.constant import INSTRUMENT_CODES, INDICATOR_NAME_TO_CODE


async def _load_data_for_content_data(db, item, is_kline, p):
    if is_kline:
        logger.debug(f'Get kline data: {item.code} {item.market} {p}')
        d = await crud.get_kline_data(db, item.code, p, item.market)
        d = [{'date': dd.date, 'value': dd.close} for dd in d]
    else:
        logger.debug(f'Get market data: {item.code} {item.instrument} {p}')
        d = await crud.get_market_data(db, INSTRUMENT_CODES[item.instrument][0])
        d = [{'date': dd.date, 'value': dd.price} for dd in d]
    return d

async def _load_data(db, item, is_kline, p):
    if isinstance(item, api_model._Contentdata):
        return await _load_data_for_content_data(db, item, is_kline, p)
    raise NotImplementedError

async def get_percentile(db, query: api_model.PercentileRequestData):

    def _resample(daily_df, period):
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

    def _cut_by_window(df, window):
        if window == -1:
            return df.copy()
        current_data = pd.Timestamp.now()
        start_date = current_data - pd.DateOffset(year=window)
        filtered = df[df['date'] >= start_date.date()]
        return filtered

    def _percentile(df):
        last_value = df['value'].iloc[-1]
        percentile = (df['value'] < last_value).sum() / df.shape[0] * 100
        return percentile

    def _calculate_pct(name, is_kline, p, w, d):
        logger.debug(f'Calculate pct of {name} {p} {w}')
        df = pd.DataFrame(d)
        if not is_kline:
            df = _resample(df, p)
        df = _cut_by_window(df, w)
        pct = _percentile(df)
        return pct

    data = query.data
    period_window = query.period_window

    res = []
    for pw in period_window:
        p, w = pw.period, pw.window

        r = {'period': p, 'window': w, 'percentile': {}}
        for cat in data:
            is_kline = cat.isKLine
            for item in cat.content:
                d = await _load_data(db, item, is_kline, p)
                pct = _calculate_pct(item.name, is_kline, p, w, d)
                r['percentile'][item.name] = pct
        res.append(r)

    return res

async def get_ucp_list(db):
    unique_market_codes = await crud.get_unique_market_code(db)
    logger.debug(f'Unique market codes: {unique_market_codes}')
    unique_market_codes = [
        UCP.from_kwargs(type_='market', code=code, column='price')
        for code in unique_market_codes
    ]

    unique_kline_codes = await crud.get_unique_kline_code(db)
    logger.debug(f'Unique kline codes: {unique_kline_codes}')
    unique_kline_codes = [
        UCP.from_kwargs(type_='kline', code=code, column='close')
        for code in unique_kline_codes
    ]

    ucps = unique_market_codes + unique_kline_codes
    indicator_res = [
        {
            'ucp': u.ucp, 'code': INDICATOR_NAME_TO_CODE[u.code] if u.type == 'market' else u.code,
        } for u in ucps]

    operation_ucp = [
        UCP.from_kwargs(type_='operation', code=op['code'], column=op['code'])
        for op in SUPPORTED_OPERATIONS
    ]
    operation_res = [
        {
            'ucp': u.ucp, 'code': u.code
        } for u in operation_ucp
    ]

    return {
        'indicator': indicator_res,
        'operation': operation_res
    }

async def get_ucp_query_result(db, ucp_string_list, sample_interval, sample_func, start, end):

    ucp_list = [UCP.from_string(u)
                for ucp_string in ucp_string_list
                for u in ucp_string.split(' ')]
    unique_ucp_data = list(set(u for u in ucp_list if u.type in ['market', 'kline']))

    async def _get_data(ucp):
        if ucp.type == 'market':
            data = await crud.get_market_data(db, ucp.code)
        elif ucp.type == 'kline':
            data = await crud.get_daily_kline_data_by_code(db, ucp.code)
        return [{'date': d.date, ucp.safe_code: getattr(d, ucp.column)} for d in data]

    def _to_df(data):
        df = pd.DataFrame(data)
        return df

    dfs = []
    for ucp in unique_ucp_data:
        data = await _get_data(ucp)
        df = _to_df(data)
        dfs.append(df)

    if dfs:
        result_df = dfs[0]
        for df in dfs[1:]:
            result_df = pd.merge(result_df, df, on='date', how='outer')
    else:
        result_df = pd.DataFrame()

    result_df['date'] = pd.to_datetime(result_df['date'])
    if start:
        result_df = result_df[result_df['date'] >= datetime.strptime(start, '%Y-%m-%d')]
    if end:
        result_df = result_df[result_df['date'] <= datetime.strptime(end, '%Y-%m-%d')]

    resample_dict = {
        'daily': 'D',
        'weekly': 'W',
        'monthly': 'M',
        'yearly': 'Y'
    }
    resampled_df = result_df.resample(resample_dict[sample_interval], on='date')

    if sample_func == 'close':
        result_df = resampled_df.last()
    elif sample_func == 'open':
        result_df = resampled_df.first()
    elif sample_func == 'high':
        result_df = resampled_df.max()
    elif sample_func == 'low':
        result_df = resampled_df.min()

    result_df = result_df.interpolate(method='linear', axis=0)
    result_df = result_df.dropna()
    result_df = result_df.reset_index()

    logger.debug(f'\n{result_df.tail(5)}')

    res = [{'date': d} for d in result_df['date']]
    for i, ucp_string in enumerate(ucp_string_list):
        expr = ''.join([UCP.from_string(u).safe_code
                        for u in ucp_string.split(' ')])
        logger.debug(f'expr {i}: {expr}')

        preprocessor = Preprocessor('df')
        executor = Executor('df')

        try:
            tree = preprocessor.preprocess(expr)
            exec_res = executor.execute(tree, result_df)
        except SyntaxError as e:
            logger.error(f'Syntax error')
            logger.error(traceback.format_exc())
            return {'status': 'fail', 'value': []}

        for j, r in enumerate(exec_res):
            value = r
            if math.isnan(r) or np.isinf(r):
                logger.warning(f'Invalid: {res[j]["date"]} {expr}: {r}')
                value = None
            res[j][f'value_{i}'] = value

    return {'status': 'success', 'value': res}

async def get_expected_return(db, query: api_model.ExpectedReturnRequestData):

    data = query.data
    p = query.p
    dt = query.dt

    data = [
        {
            'code': item.code,
            'df': pd.DataFrame(await _load_data(db, item, cat.isKLine, 'daily'))
        } for cat in data for item in cat.content
    ]

    def _f(code, df, p, dt):
        df['value'] = df['value'].interpolate(method='linear')
        df = df.dropna()
        log_ret = np.log(df['value'] / df['value'].shift(1))
        log_ret = log_ret.dropna()
        mu, sigma = estimate_normal_distribution(log_ret)
        n = log_ret.shape[0]
        exp = math.exp(exp_geometric_random_walk(mu, dt)) - 1

        std = std_geometric_random_walk(sigma, dt)
        lower, upper = normal_interval(p)
        lower = math.exp(mu * dt + lower * std / n ** 0.5) - 1
        upper = math.exp(mu * dt + upper * std / n ** 0.5) - 1

        return {
            'code': code,
            'exp': exp,
            'lower': lower,
            'upper': upper
        }

    res = Parallel(n_jobs=-1)(delayed(_f)(item['code'], item['df'], p, dt) for item in data)
    logger.debug(f'Prob growth rate:')
    for r in res:
        logger.debug(f'{r["code"]} {r["exp"]:.4f} ({r["lower"]:.4f}--{r["upper"]:.4f})')

    return res
