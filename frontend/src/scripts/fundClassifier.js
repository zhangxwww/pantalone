function isBond (fund) {
    return fund.indexOf('债') !== -1
        || fund.indexOf('一年持有') !== -1;
}

function isUSStock (fund) {
    return fund.indexOf('美国') !== -1 && fund.indexOf('股票') !== -1
        || fund.indexOf('纳斯达克') !== -1
        || fund.indexOf('标普') !== -1
        || fund.indexOf('道琼斯') !== -1;
}

function isGold (fund) {
    return fund.indexOf('黄金') !== -1;
}

function isDefensive (fund) {
    return fund.indexOf('红利') !== -1
        || fund.indexOf('低波') !== -1
        || fund.indexOf('银行') !== -1
        || fund.indexOf('价值') !== -1
        || fund.indexOf('现金流') !== -1;
}

function isOther (fund) {
    console.warn(`Classifying fund as 'Other': ${fund}`);
    return true
}

function isGrowth (fund) {
    return fund.indexOf('中证2000') !== -1
        || fund.indexOf('创业板') !== -1
        || fund.indexOf('科技') !== -1;
}

const classMap = {
    "黄金": isGold,
    "债券": isBond,
    "美股": isUSStock,
    "价值": isDefensive,
    "成长": isGrowth,
    "其他": isOther,
};

export function classifyFund (fund) {
    for (const [className, classify] of Object.entries(classMap)) {
        if (classify(fund)) {
            return className;
        }
    }
    throw new Error(`Unknown fund class: ${fund}`);
}

export const allClasses = Object.keys(classMap);