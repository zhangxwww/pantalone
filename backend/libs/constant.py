from datetime import datetime


INDEX_CODES = [
    '000001',  # 上证指数
    '000012',  # 国债指数
]

KLINE_START = {
    'daily': datetime.strptime('1997-01-01', '%Y-%m-%d').date(),
    'weekly': datetime.strptime('1997-01-01', '%Y-%m-%d').date(),
    'monthly': datetime.strptime('1997-01-01', '%Y-%m-%d').date(),
}

CURRENCY_DICT = {
    'USD': '美元',
    'EUR': '欧元',
    'JPY': '日元',
    'GBP': '英镑',
    'HKD': '港币',
    'THB': '泰国铢'
}

INSTRUMENT_CODES = {
    'LPR': ['lpr_1y', 'lpr_5y', 'short_term_rate', 'mid_term_rate'],
    **{k: [v] for k, v in CURRENCY_DICT.items()},
    'leverage-CN': [
        'leverage_resident', 'leverage_non_financial', 'leverage_government',
        'leverage_central_government', 'leverage_local_government',
        'leverage_real_economy', 'leverage_financial_assets',
        'leverage_financial_liabilities'
    ]
}