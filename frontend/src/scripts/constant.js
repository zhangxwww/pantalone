export const FOLLOWED_DATA = [
    {
        category: 'A股指数',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '上证综指',
                code: '000001',
                market: 'index-CN'
            },
            {
                name: '深证成指',
                code: '399001',
                market: 'index-CN'
            },
            {
                name: '创业板指',
                code: '399006',
                market: 'index-CN'
            },
            {
                name: '沪深300',
                code: '000300',
                market: 'index-CN'
            },
            {
                name: '北证50',
                code: '899050',
                market: 'index-CN'
            },
            {
                name: '科创50',
                code: '000688',
                market: 'index-CN'
            },
            {
                name: '中证A500',
                code: '000510',
                market: 'index-CN'
            },
            {
                name: '中证1000',
                code: '000852',
                market: 'index-CN'
            },
            {
                name: '中证2000',
                code: '932000',
                market: 'index-CN'
            }
        ]
    },
    {
        category: '美股指数',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '纳斯达克综合指数',
                code: '.IXIC',
                market: 'index-US'
            },
            {
                name: '道琼斯工业指数',
                code: '.DJI',
                market: 'index-US'
            },
            {
                name: '标普500指数',
                code: '.INX',
                market: 'index-US'
            },
            {
                name: '纳斯达克100指数',
                code: '.NDX',
                market: 'index-US'
            }
        ]
    },
    {
        category: '港股指数',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '恒生指数',
                code: 'HSI',
                market: 'index-HK'
            },
            {
                name: '恒生科技指数',
                code: 'HSTECH',
                market: 'index-HK'
            },
            {
                name: '恒生中国内地银行指数',
                code: 'HSMBI',
                market: 'index-HK'
            },
            {
                name: '恒生中国内地石油及天然气指数',
                code: 'HSMOGI',
                market: 'index-HK'
            },
            {
                name: '恒生中国内地地产指数',
                code: 'HSMPI',
                market: 'index-HK'
            }
        ]
    },
    {
        category: '波动率指数',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '50ETF期权波动率指数QVIX',
                code: '50ETF',
                market: 'index-qvix'
            },
            {
                name: '300ETF期权波动率指数QVIX',
                code: '300ETF',
                market: 'index-qvix'
            }
        ]
    },
    {
        category: '债券指数',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '国债指数',
                code: '000012',
                market: 'index-CN'
            },
            {
                name: '企债指数',
                code: '000013',
                market: 'index-CN'
            },
            {
                name: '公司债指',
                code: '000923',
                market: 'index-CN'
            }
        ]
    },
    {
        category: '商品期货',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '黄金连续',
                code: 'AU0',
                market: 'future-zh'
            },
            {
                name: '白银连续',
                code: 'AG0',
                market: 'future-zh'
            },
            {
                name: '铜连续',
                code: 'CU0',
                market: 'future-zh'
            },
            {
                name: '上海原油连续',
                code: 'SC0',
                market: 'future-zh'
            },
        ]
    },
    {
        category: '股指期货',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '沪深300指数期货',
                code: 'IF0',
                market: 'future-zh'
            },
            {
                name: '上证50指数期货',
                code: 'IH0',
                market: 'future-zh'
            },
            {
                name: '中证500指数期货',
                code: 'IC0',
                market: 'future-zh'
            }
        ]
    },
    {
        category: '国债期货',
        isKLine: true,
        skipPercentile: false,
        content: [
            {
                name: '5年期国债期货',
                code: 'TF0',
                market: 'future-zh'
            },
            {
                name: '2年期国债期货',
                code: 'TS0',
                market: 'future-zh'
            }
        ]
    },
    {
        category: '利率',
        isKLine: false,
        skipPercentile: true,
        content: [
            {
                name: 'LPR品种',
                code: '',
                instrument: 'LPR'
            }
        ]
    },
    {
        category: '外汇',
        isKLine: false,
        skipPercentile: false,
        content: [
            {
                name: '美元',
                code: 'USD/CNY',
                instrument: 'USD'
            },
            {
                name: '欧元',
                code: 'EUR/CNY',
                instrument: 'EUR'
            },
            {
                name: '日元',
                code: 'JPY/CNY',
                instrument: 'JPY'
            },
            {
                name: '英镑',
                code: 'GBP/CNY',
                instrument: 'GBP'
            },
            {
                name: '港币',
                code: 'HKD/CNY',
                instrument: 'HKD'
            },
            {
                name: '泰国铢',
                code: 'THB/CNY',
                instrument: 'THB'
            }
        ]
    },
    {
        category: '宏观',
        isKLine: false,
        skipPercentile: true,
        content: [
            {
                name: '宏观杠杆率',
                code: '',
                instrument: 'leverage-CN'
            },
            {
                name: '失业率',
                code: '',
                instrument: 'unemployment-rate-CN'
            },
            {
                name: '社融增量',
                code: '',
                instrument: 'AFRE-CN'
            },
            {
                name: 'GDP年率',
                code: '',
                instrument: 'GDP-CN'
            },
            {
                name: 'CPI年率',
                code: '',
                instrument: 'CPI-yearly-CN'
            },
            {
                name: 'CPI月率',
                code: '',
                instrument: 'CPI-monthly-CN'
            },
            {
                name: 'PPI年率',
                code: '',
                instrument: 'PPI-CN'
            },
            {
                name: '以美元计算出口年率',
                code: '',
                instrument: 'EXP-CN'
            },
            {
                name: '以美元计算进口年率',
                code: '',
                instrument: 'IMP-CN'
            },
            {
                name: '规模以上工业增加值年率',
                code: '',
                instrument: 'industrial-production-yoy-CN'
            },
            {
                name: '官方制造业PMI',
                code: '',
                instrument: 'PMI-CN'
            },
            {
                name: '中国官方非制造业PMI',
                code: '',
                instrument: 'non-man-PMI-CN'
            },
            {
                name: '外汇储备（亿美元）',
                code: '',
                instrument: 'fx-CN'
            },
            {
                name: 'M2货币供应年率',
                code: '',
                instrument: 'M2-CN'
            },
        ]
    },
    {
        category: '全球宏观',
        isKLine: false,
        skipPercentile: true,
        content: []
    }
];

export const DEFUALT_COLOR = ['#50c48f', '#26ccd8', '#3685fe', '#9977ef', '#f5616f', '#f7b13f', '#f9e264', '#f47a75', '#009db2', '#024b51', '#0780cf', '#765005'];

export const FOLLOWED_DATA_NAME_2_CATEGORY = {};
export const PERCENTILE_CHART_CATEGORY_COLOR = {};
const _CATEGORIES = [];
for (const data of FOLLOWED_DATA) {
    const category = data.category;
    _CATEGORIES.push(category);
    for (const content of data.content) {
        FOLLOWED_DATA_NAME_2_CATEGORY[content.name] = category;
    }
    const catIndex = _CATEGORIES.findIndex((cat) => cat === category);
    PERCENTILE_CHART_CATEGORY_COLOR[category] = DEFUALT_COLOR[catIndex];
}


export const PERCENTILE_PERIOD_WINDOW = [
    {
        'period': 'daily',
        'window': 1
    },
    {
        'period': 'daily',
        'window': 3
    },
    {
        'period': 'daily',
        'window': -1
    },
    {
        'period': 'weekly',
        'window': 1
    },
    {
        'period': 'weekly',
        'window': 5
    },
    {
        'period': 'weekly',
        'window': -1
    },
    {
        'period': 'monthly',
        'window': 3
    },
    {
        'period': 'monthly',
        'window': 10
    },
    {
        'period': 'monthly',
        'window': -1
    }
];

export const PERCENTILE_CHART_TRANSLATION = {
    'daily': '当日',
    'weekly': '当周',
    'monthly': '当月',
};

export const INSTRUMENT_INDICATOR_TRANSLATION_SHORT = {
    'lpr_1y': '1年期LPR',
    'lpr_5y': '5年期LPR',
    'short_term_rate': '短期贷款利率',
    'mid_term_rate': '中长期贷款利率',
    '美元': 'USD/CNY',
    '欧元': 'EUR/CNY',
    '日元': 'JPY/CNY',
    '英镑': 'GBP/CNY',
    '港币': 'HKD/CNY',
    '泰国铢': 'THB/CNY',
    'leverage_resident': '居民部门',
    'leverage_non_financial': '非金融企业部门',
    'leverage_government': '政府部门',
    'leverage_central_government': '中央政府',
    'leverage_local_government': '地方政府',
    'leverage_real_economy': '实体经济部门',
    'leverage_financial_assets': '金融部门资产方',
    'leverage_financial_liabilities': '金融部门负债方',
    'national_urban_unemployment_rate': '全国城镇',
    '31_major_cities_urban_unemployment_rate': '31个大城市',
    'national_urban_local_unemployment_rate': '本地户籍',
    'national_urban_migrant_unemployment_rate': '外来户籍',
    '16_24_urban_unemployment_rate': '16-24岁',
    '25_59_urban_unemployment_rate': '25-59岁',
    '16_24_urban_unemployment_rate_excluding_students': '16-24岁不含在校生',
    '25_29_urban_unemployment_rate_excludng_students': '25-29岁不含在校生',
    '30_59_urban_unemployment_rate_excludng_students': '30-59岁不含在校生',
    'aggregate_financing_to_the_real_economy': '社会融资规模增量',
    'renminbi_loan': '人民币贷款',
    'entrusted_foreign_currency_loan': '委托贷款外币贷款',
    'entrusted_loan': '委托贷款',
    'trust_loan': '信托贷款',
    'undiscounted_bank_acceptance_bill': '未贴现银行承兑汇票',
    'corporate_bonds': '企业债券',
    'domestic_stock_financing_for_non_financial_enterprises': '非金融企业境内股票融资',
    'gdp_cn_current': '今值',
    'gdp_cn_predict': '预测值',
    'gdp_cn_previous': '前值',
    'cpi_yearly_cn_current': '今值',
    'cpi_yearly_cn_predict': '预测值',
    'cpi_yearly_cn_previous': '前值',
    'cpi_monthly_cn_current': '今值',
    'cpi_monthly_cn_predict': '预测值',
    'cpi_monthly_cn_previous': '前值',
    'ppi_cn_current': '今值',
    'ppi_cn_predict': '预测值',
    'ppi_cn_previous': '前值',
    'exp_cn_current': '今值',
    'exp_cn_predict': '预测值',
    'exp_cn_previous': '前值',
    'imp_cn_current': '今值',
    'imp_cn_predict': '预测值',
    'imp_cn_previous': '前值',
    'ipy_cn_current': '今值',
    'ipy_cn_predict': '预测值',
    'ipy_cn_previous': '前值',
    'pmi_cn_current': '今值',
    'pmi_cn_predict': '预测值',
    'pmi_cn_previous': '前值',
    'nPMI_cn_current': '今值',
    'nPMI_cn_predict': '预测值',
    'nPMI_cn_previous': '前值',
    'fx_cn_current': '今值',
    'fx_cn_predict': '预测值',
    'fx_cn_previous': '前值',
    'm2_cn_current': '今值',
    'm2_cn_predict': '预测值',
    'm2_cn_previous': '前值',
};
for (const cat of FOLLOWED_DATA) {
    for (const content of cat.content) {
        if (!INSTRUMENT_INDICATOR_TRANSLATION_SHORT[content.code]) {
            INSTRUMENT_INDICATOR_TRANSLATION_SHORT[content.code] = content.name;
        }
    }
}

export const INSTRUMENT_INDICATOR_TRANSLATION_LONG = {};
for (const [raw, t] of Object.entries(INSTRUMENT_INDICATOR_TRANSLATION_SHORT)) {
    if (raw.includes('leverage')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `${t}杠杆率`;
    } else if (raw.includes('unemployment')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `${t}失业率`;
    } else if (raw.includes('gdp')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `GDP${t}`;
    } else if (raw.includes('cpi_yearly')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `CPI年率${t}`;
    } else if (raw.includes('cpi_monthly')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `CPI月率${t}`;
    } else if (raw.includes('ppi')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `PPI年率${t}`;
    } else if (raw.includes('exp')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `以美元计算出口年率${t}`;
    } else if (raw.includes('imp')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `以美元计算进口年率${t}`;
    } else if (raw.includes('ipy')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `规模以上工业增加值年率${t}`;
    } else if (raw.includes('pmi')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `官方制造业PMI${t}`;
    } else if (raw.includes('nPMI')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `官方非制造业PMI${t}`;
    } else if (raw.includes('fx')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `外汇储备${t}`;
    } else if (raw.includes('m2')) {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = `M2货币供应年率${t}`;
    } else {
        INSTRUMENT_INDICATOR_TRANSLATION_LONG[raw] = t;
    }
}
