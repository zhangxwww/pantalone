function mockjson () {
    return {
        cashData: [
            {
                name: "中国银行",
                amount: 100000,
                beginningTime: "2021-01-01"
            },
            {
                name: "中国银行",
                amount: 200000,
                beginningTime: "2023-01-01"
            },
            {
                name: "工商银行",
                amount: 200000,
                beginningTime: "2021-06-01"
            },
            {
                name: "建设银行",
                amount: 300000,
                beginningTime: "2022-01-01"
            }
        ],
        monetaryFundData: [
            {
                name: "华夏基金",
                beginningAmount: 100000,
                beginningTime: "2021-01-01",
                currentAmount: 200000,
                fastRedemption: true
            },
            {
                name: "招商基金",
                beginningAmount: 200000,
                beginningTime: "2021-01-01",
                currentAmount: 300000,
                fastRedemption: false
            },
        ],
        fixedDepositData: [
            {
                name: "中国银行",
                beginningAmount: 100000,
                rate: 0.1,
                maturity: 365,
                beginningTime: "2021-01-01",
            }
        ]
    }
}


function mock () {
    return {
        cashData: [
            {
                name: "中国银行",
                amount: 100000
            },
            {
                name: "工商银行",
                amount: 200000
            },
            {
                name: "建设银行",
                amount: 300000
            }
        ],
        monetaryFundData: [
            {
                name: "华夏基金",
                beginningAmount: 100000,
                beginningTime: "2021-01-01",
                currentAmount: 200000,
                annualizedReturnRate: 0.1
            },
            {
                name: "招商基金",
                beginningAmount: 200000,
                beginningTime: "2021-01-01",
                currentAmount: 300000,
                annualizedReturnRate: 0.2
            },
        ],
        fixedDepositData: [
            {
                name: "中国银行",
                beginningAmount: 100000,
                rate: 0.1,
                maturity: 365,
                beginningTime: "2021-01-01",
                endingTime: "2022-01-01",
                residualMaturaty: 100,
                endingAmount: 110000
            }
        ]
    }
}


// eslint-disable-next-line no-unused-vars
class CashDataRecord {
    constructor(name, amount, beginningTime) {
        this.name = name;
        this.amount = amount;
        this.beginningTime = new Date(beginningTime);
        this.endTime = new Date('2100-01-01');
    }

    // eslint-disable-next-line no-unused-vars
    getInfo (date) {
        return {
            name: this.name,
            amount: this.amount,
            liquidity: 0,
            returnRate: 0,
            beginningTime: this.beginningTime,
            endTime: this.endTime
        };

    }
}


// eslint-disable-next-line no-unused-vars
class MonetaryFundDataRecored {
    constructor(name, beginningAmount, currentAmount, beginningTime, fastRedemption) {
        this.name = name;
        this.beginningAmount = beginningAmount;
        this.currentAmount = currentAmount;
        this.beginningTime = new Date(beginningTime);
        this.endTime = new Date('2100-01-01');
        this.fastRedemption = fastRedemption;
    }

    getAnnualReturn (date) {
        const ret = (this.currentAmount - this.beginningAmount) / this.beginningAmount;
        const days = (date - this.beginningTime) / (1000 * 3600 * 24);
        return ret / days * 365;
    }
}


// eslint-disable-next-line no-unused-vars
class FixedDepositDataRecord {
    constructor(name, beginningAmount, rate, beginningTime, maturity) {
        this.name = name;
        this.beginningAmount = beginningAmount;
        this.rate = rate;
        this.beginningTime = new Date(beginningTime);
        this.endTime = new Date(beginningTime);
        this.endTime.setDate(this.endTime.getDate() + maturity);
        this.maturity = maturity;
    }

    // eslint-disable-next-line no-unused-vars
    getAnnualReturn (date) {
        return this.rate;
    }
}


class Data {
    // eslint-disable-next-line no-unused-vars
    constructor(json) {
        this.cashDataRecords = [];
        this.monetaryDataRecords = [];
        this.fixedDepositDataRecords = [];
        this.parseDataFromJson(mockjson());
    }

    getData () {
        return mock();
    }

    // eslint-disable-next-line no-unused-vars
    parseDataFromJson (json) {
        // TODO: Parse data from json
        // return mock();
    }

    // eslint-disable-next-line no-unused-vars
    addData (data, type) {
        //
    }

    sampleDates () {
        let dates = [];
        let currentDate = new Date();

        for (let i = 0; i < 12; i++) {
            let newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
            dates.unshift(newDate);
        }
        return dates;
    }


    getLatestRecord (data, date) {
        let res = [];
        let found = [];
        const beforeDate = data.filter(r => r.beginningTime >= date && r.endTime <= date);
        for (let i = 0; i < beforeDate.length; i++) {
            let record = beforeDate[i];
            if (found.indexOf(record.name) === -1) {
                res.push(record);
                found.push(record.name);
            } else {
                res = res.filter(r => r.name !== record.name);
                res.push(record);
            }
        }
        return res;
    }

    getAssetChanges () {
        let dates = this.sampleDates();
        let assetChanges = [];
        for (let i = 0; i < dates.length; i++) {
            let date = dates[i];
            let assetChange = {
                date: date,
                cash: 0,
                monetary: 0,
                fixedDeposit: 0
            };

            const cashRecord = this.getLatestRecord(this.cashDataRecords, date);
            const monetaryRecord = this.getLatestRecord(this.monetaryDataRecords, date);
            const fixedDepositRecord = this.getLatestRecord(this.fixedDepositDataRecords, date);

            for (let j = 0; j < cashRecord.length; j++) {
                assetChange.cash += cashRecord[j].amount;
            }

            for (let j = 0; j < monetaryRecord.length; j++) {
                assetChange.monetary += monetaryRecord[j].currentAmount;
            }

            for (let j = 0; j < fixedDepositRecord.length; j++) {
                assetChange.fixedDeposit += fixedDepositRecord[j].beginningAmount;
            }

            assetChanges.push(assetChange);
        }
        return assetChanges;
    }
}

export default Data;