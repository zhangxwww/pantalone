function isBond (fund) {
    return fund.indexOf('债') !== -1;
}

function isUSStock (fund) {
    return fund.indexOf('美国') !== -1 && fund.indexOf('股票') !== -1 || fund.indexOf('纳斯达克') !== -1 || fund.indexOf('标普') !== -1 || fund.indexOf('道琼斯') !== -1;
}

function isGold (fund) {
    return fund.indexOf('黄金') !== -1;
}

function isGlobal (fund) {
    return fund.indexOf('全球') !== -1 && fund.indexOf('股票') !== -1 || fund.indexOf('日本') !== -1;
}

function isDefensive (fund) {
    return fund.indexOf('红利') !== -1 || fund.indexOf('低波') !== -1 || fund.indexOf('银行') !== -1 || fund.indexOf('现金流') !== -1;
}

function isMixed (fund) {
    return fund.indexOf('混合') !== -1;
}

function isGrowth (fund) {
    return fund.indexOf('中证2000') !== -1;
}

const classMap = {
    "债券": isBond,
    "美股": isUSStock,
    "黄金": isGold,
    "防御型": isDefensive,
    "成长型": isGrowth,
    "混合": isMixed,
    "全球": isGlobal
};

export function classifyFund (fund) {
    for (const [className, classify] of Object.entries(classMap)) {
        if (classify(fund)) {
            return className;
        }
    }
}

export const allClasses = Object.keys(classMap);