const FOLLOWED_DATA = [
    {
        category: 'A股指数',
        isKLine: true,
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
        content: [
            {
                name: '宏观杠杆率',
                code: '',
                instrument: 'leverage-CN'
            }
        ]
    },
    {
        category: '全球宏观',
        isKLine: false,
        content: []
    }
]

export {
    FOLLOWED_DATA
}