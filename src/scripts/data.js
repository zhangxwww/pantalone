function clone (x) {
    return JSON.parse(JSON.stringify(x));
}

function timeFormat (t, short = false) {
    let year = t.getFullYear();
    let month = t.getMonth() + 1;
    let day = t.getDate();
    let formatted;
    if (short) {
        formatted = `${year}/${month < 10 ? '0' + month : month}`;
    } else {
        formatted = `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`;
    }
    return formatted;
}

function mockjson () {
    return {
        cashData: [
            {
                id: 1,
                history: [
                    {
                        name: "中国银行",
                        amount: 100000.00,
                        beginningTime: "2021-06-01"
                    },
                    {
                        name: "中国银行",
                        amount: 200000.00,
                        beginningTime: "2023-06-01"
                    }
                ]
            },
            {
                id: 2,
                history: [
                    {
                        name: "工商银行",
                        amount: 200000.00,
                        beginningTime: "2021-06-01"
                    }
                ]
            },
            {
                id: 3,
                history: [
                    {
                        name: "建设银行",
                        amount: 300000.00,
                        beginningTime: "2022-01-01"
                    }
                ]
            }
        ],
        monetaryFundData: [
            {
                id: 1,
                history: [
                    {
                        name: "华夏基金",
                        beginningAmount: 100000.00,
                        beginningTime: "2021-01-01",
                        currentAmount: 200000.00,
                        currentTime: "2021-06-01",
                        fastRedemption: true,
                        holding: true
                    },
                    {
                        name: "华夏基金",
                        beginningAmount: 100000.00,
                        beginningTime: "2021-01-01",
                        currentAmount: 300000.00,
                        currentTime: "2022-06-01",
                        fastRedemption: true,
                        holding: true
                    }
                ]
            },
            {
                id: 2,
                history: [
                    {
                        name: "招商基金",
                        beginningAmount: 200000.00,
                        beginningTime: "2021-01-01",
                        currentAmount: 300000.00,
                        currentTime: "2023-01-01",
                        fastRedemption: false,
                        holding: false
                    }
                ]
            },
            {
                id: 3,
                history: [
                    {
                        name: "天弘基金",
                        beginningAmount: 40000.00,
                        beginningTime: "2022-01-01",
                        currentAmount: 50000.00,
                        currentTime: "2024-01-01",
                        fastRedemption: false,
                        holding: true
                    }
                ]
            }
        ],
        fixedDepositData: [
            {
                id: 1,
                history: [
                    {
                        name: "中国银行",
                        beginningAmount: 100000.00,
                        rate: 0.01,
                        maturity: 365,
                        beginningTime: "2021-01-01",
                    }
                ]
            },
            {
                id: 2,
                history: [
                    {
                        name: "工商银行",
                        beginningAmount: 200000.00,
                        rate: 0.02,
                        maturity: 365,
                        beginningTime: "2024-01-01",
                    }
                ]
            },
            {
                id: 3,
                history: [
                    {
                        name: "建设银行",
                        beginningAmount: 300000.00,
                        rate: 0.03,
                        maturity: 30,
                        beginningTime: "2024-06-01",
                    }
                ]
            },
            {
                id: 4,
                history: [
                    {
                        name: "农业银行",
                        beginningAmount: 100000.00,
                        rate: 0.04,
                        maturity: 90,
                        beginningTime: "2024-04-01",
                    }
                ]
            },
            {
                id: 5,
                history: [
                    {
                        name: "交通银行",
                        beginningAmount: 200000.00,
                        rate: 0.05,
                        maturity: 180,
                        beginningTime: "2024-03-01",
                    }
                ]
            },
            {
                id: 6,
                history: [
                    {
                        name: "邮政储蓄",
                        beginningAmount: 300000.00,
                        rate: 0.06,
                        maturity: 700,
                        beginningTime: "2024-01-01",
                    }
                ]
            }
        ]
    }
}

class Data {
    // eslint-disable-next-line no-unused-vars
    constructor(json) {
        // this.data = json;
        this.json = mockjson();
        this.data = this.prepareData();
    }

    prepareData () {
        const data = clone(this.json);
        for (let cData of data.cashData) {
            for (let cHis of cData.history) {
                cHis.amountFmt = cHis.amount.toFixed(2);
                cHis.beginningTime = new Date(cHis.beginningTime);
            }
        }
        for (let mData of data.monetaryFundData) {
            for (let mHis of mData.history) {
                mHis.beginningTime = new Date(mHis.beginningTime);
                mHis.currentTime = new Date(mHis.currentTime);
                const ret = (mHis.currentAmount - mHis.beginningAmount) / mHis.beginningAmount;
                const days = (mHis.currentTime - mHis.beginningTime) / (1000 * 3600 * 24);
                mHis.annualizedReturnRate = ret / days * 365;

                mHis.beginningTimeFmt = timeFormat(mHis.beginningTime);
                mHis.annualizedReturnRateFmt = (mHis.annualizedReturnRate * 100).toFixed(2) + '%';
                mHis.beginningAmountFmt = mHis.beginningAmount.toFixed(2);
                mHis.currentAmountFmt = mHis.currentAmount.toFixed(2);
            }
        }
        for (let fData of data.fixedDepositData) {
            for (let fHis of fData.history) {
                fHis.beginningTime = new Date(fHis.beginningTime);
                fHis.endingAmount = fHis.beginningAmount * (1 + fHis.rate * fHis.maturity / 365);
                fHis.endingTime = new Date(fHis.beginningTime);
                fHis.endingTime.setDate(fHis.endingTime.getDate() + fHis.maturity);

                fHis.residualMaturaty = Math.ceil((fHis.endingTime - new Date()) / (1000 * 3600 * 24));

                fHis.beginningTimeFmt = timeFormat(fHis.beginningTime);
                fHis.endingTimeFmt = timeFormat(fHis.endingTime);

                fHis.beginningAmountFmt = fHis.beginningAmount.toFixed(2);
                fHis.endingAmountFmt = fHis.endingAmount.toFixed(2);

                fHis.rateFmt = (fHis.rate * 100).toFixed(2) + '%';
            }
        }
        return data;
    }

    getData () {
        const data = {
            cashData: [],
            monetaryFundData: [],
            fixedDepositData: []
        };
        for (let cdata of this.data.cashData) {
            data.cashData.push(cdata.history[cdata.history.length - 1]);
        }
        for (let mdata of this.data.monetaryFundData) {
            // filter: holding === true
            const last = mdata.history[mdata.history.length - 1];
            if (last.holding !== true) {
                continue;
            }
            data.monetaryFundData.push(last);
        }
        for (let fdata of this.data.fixedDepositData) {
            // filter: endingTime >= now
            const last = fdata.history[fdata.history.length - 1];
            if (new Date() > last.endingTime) {
                continue;
            }
            data.fixedDepositData.push(last);
        }
        return data;
    }

    // eslint-disable-next-line no-unused-vars
    addData (data, type) {
        //
    }

    sampleDates () {
        let dates = [];
        let currentDate = new Date();

        for (let i = 0; i < 60; i += 3) {
            let newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
            dates.unshift(newDate);
        }
        return dates;
    }

    getAssetChangeData () {
        const dates = this.sampleDates();
        const cashData = [];
        const monetaryFundData = [];
        const fixedDepositData = [];

        for (let date of dates) {
            let cash = 0;
            for (let cData of this.data.cashData) {
                const candidate = cData.history.filter(h => h.beginningTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.amount > 0) {
                    cash += d.amount;
                }
            }
            cashData.push(cash);

            let monetaryFund = 0;
            for (let mData of this.data.monetaryFundData) {
                const first = mData.history[0];
                let add = 0;
                if (first.beginningTime < date) {
                    add = first.beginningAmount;
                }

                const candidate = mData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.currentAmount > 0) {
                    add = d.currentAmount;
                }
                monetaryFund += add;
            }
            monetaryFundData.push(monetaryFund);

            let fixedDeposit = 0;
            for (let fData of this.data.fixedDepositData) {
                const candidate = fData.history.filter(h => h.beginningTime <= date && h.endingTime >= date);
                const d = candidate[candidate.length - 1];
                if (d && d.beginningAmount > 0) {
                    fixedDeposit += d.beginningAmount;
                }
            }
            fixedDepositData.push(fixedDeposit);
        }
        return {
            time: dates.map(t => timeFormat(t, true)),
            cashData: cashData,
            monetaryFundData: monetaryFundData,
            fixedDepositData: fixedDepositData
        }
    }

    getResidualMaturityData () {
        const maturitiyData = [
            { name: "T+0", amount: 0 },
            { name: "T+1", amount: 0 },
            { name: "30日内", amount: 0 },
            { name: "90日内", amount: 0 },
            { name: "180日内", amount: 0 },
            { name: "365日内", amount: 0 },
            { name: "365日以上", amount: 0 }
        ];
        for (let cData of this.data.cashData) {
            const last = cData.history[cData.history.length - 1];
            maturitiyData[0].amount += last.amount;
        }
        for (let mData of this.data.monetaryFundData) {
            const last = mData.history[mData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.fastRedemption) {
                maturitiyData[0].amount += last.currentAmount;
            } else {
                maturitiyData[1].amount += last.currentAmount;
            }
        }
        for (let fData of this.data.fixedDepositData) {
            const last = fData.history[fData.history.length - 1];
            if (last.maturity < 0) {
                continue;
            } else if (last.maturity <= 30) {
                maturitiyData[2].amount += last.beginningAmount;
            } else if (last.maturity <= 90) {
                maturitiyData[3].amount += last.beginningAmount;
            } else if (last.maturity <= 180) {
                maturitiyData[4].amount += last.beginningAmount;
            } else if (last.maturity <= 365) {
                maturitiyData[5].amount += last.beginningAmount;
            } else {
                maturitiyData[6].amount += last.beginningAmount;
            }
        }
        maturitiyData.forEach(item => {
            item.value = item.amount;
        });
        return maturitiyData;
    }
}

export default Data;