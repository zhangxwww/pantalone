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
    ],
    'unemployment-rate-CN': [
        'national_urban_unemployment_rate',
        '31_major_cities_urban_unemployment_rate',
        'national_urban_local_unemployment_rate',
        'national_urban_migrant_unemployment_rate',
        '16_24_urban_unemployment_rate',
        '25_59_urban_unemployment_rate',
        '16_24_urban_unemployment_rate_excluding_students',
        '25_29_urban_unemployment_rate_excludng_students',
        '30_59_urban_unemployment_rate_excludng_students',
    ],
    'AFRE-CN': [
        'aggregate_financing_to_the_real_economy',
        'renminbi_loan',
        'entrusted_foreign_currency_loan',
        'entrusted_loan',
        'trust_loan',
        'undiscounted_bank_acceptance_bill',
        'corporate_bonds',
        'domestic_stock_financing_for_non_financial_enterprises',
    ],
    'GDP-CN': [
        'gdp_cn_current',
        'gdp_cn_predict',
        'gdp_cn_previous'
    ],
    'CPI-yearly-CN': [
        'cpi_yearly_cn_current',
        'cpi_yearly_cn_predict',
        'cpi_yearly_cn_previous'
    ],
    'CPI-monthly-CN': [
        'cpi_monthly_cn_current',
        'cpi_monthly_cn_predict',
        'cpi_monthly_cn_previous'
    ],
    'PPI-CN': [
        'ppi_cn_current',
        'ppi_cn_predict',
        'ppi_cn_previous'
    ],
    'EXP-CN': [
        'exp_cn_current',
        'exp_cn_predict',
        'exp_cn_previous'
    ],
    'IMP-CN': [
        'imp_cn_current',
        'imp_cn_predict',
        'imp_cn_previous'
    ],
    'industrial-production-yoy-CN': [
        'ipy_cn_current',
        'ipy_cn_predict',
        'ipy_cn_previous'
    ],
    'PMI-CN': [
        'pmi_cn_current',
        'pmi_cn_predict',
        'pmi_cn_previous'
    ],
    'non-man-PMI-CN': [
        'nPMI_cn_current',
        'nPMI_cn_predict',
        'nPMI_cn_previous'
    ],
    'fx-CN': [
        'fx_cn_current',
        'fx_cn_predict',
        'fx_cn_previous'
    ],
    'M2-CN': [
        'm2_cn_current',
        'm2_cn_predict',
        'm2_cn_previous'
    ]
}