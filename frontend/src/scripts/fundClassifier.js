export function classifyFund (fund) {
    if (fund.indexOf('债') !== -1) {
        return '债券';
    } else if (fund.indexOf('美国') !== -1 && fund.indexOf('股票') !== -1 || fund.indexOf('纳斯达克') !== -1 || fund.indexOf('标普') !== -1 || fund.indexOf('道琼斯') !== -1) {
        return '美股';
    } else if (fund.indexOf('黄金') !== -1) {
        return '黄金';
    } else if (fund.indexOf('全球') !== -1 && fund.indexOf('股票') !== -1 || fund.indexOf('日本') !== -1) {
        return '全球';
    } else if (fund.indexOf('红利低波') !== -1) {
        return '红利低波';
    } else if (fund.indexOf('银行') !== -1) {
        return '银行';
    } else if (fund.indexOf('混合') !== -1) {
        return '混合';
    } else if (fund.indexOf('中证2000') !== -1) {
        return '中证2000';
    }
}

export const allClasses = [
    "黄金", "美股", "中证2000", "红利低波", "银行", "混合", "债券", "全球"
]