import statistic from './statistic.js';
import { timeFormat } from './formatter.js';
import {
    getChinaBondYieldDataRequest,
    loadDataRequest,
    uploadRequest,
    addDataRequest,
    getNormalIntervalRequest,
} from './requests.js';


function clone (x) {
    return JSON.parse(JSON.stringify(x));
}


class Data {
    async load () {
        this.json = await loadDataRequest();
        this.data = this.prepareData();
    }

    prepareData () {
        const data = clone(this.json);

        if (!data.cashData) {
            data.cashData = [];
        }
        if (!data.monetaryFundData) {
            data.monetaryFundData = [];
        }
        if (!data.fixedDepositData) {
            data.fixedDepositData = [];
        }
        if (!data.fundData) {
            data.fundData = [];
        }

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
                mHis.beginningNetValue = mHis.beginningAmount / mHis.beginningShares;
                mHis.currentNetValue = mHis.currentAmount / mHis.currentShares;
                const ret = (mHis.currentNetValue - mHis.beginningNetValue) / mHis.beginningNetValue;
                const days = (mHis.currentTime - mHis.beginningTime) / (1000 * 3600 * 24);
                mHis.annualizedReturnRate = ret / days * 365;

                mHis.beginningTimeFmt = timeFormat(mHis.beginningTime);
                mHis.annualizedReturnRateFmt = (mHis.annualizedReturnRate * 100).toFixed(2) + '%';
                mHis.currentAmountFmt = mHis.currentAmount.toFixed(2);
                mHis.fastRedemptionFmt = mHis.fastRedemption ? '是' : '否';
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
        for (let uData of data.fundData) {
            for (let uHis of uData.history) {
                uHis.beginningTime = new Date(uHis.beginningTime);
                uHis.currentTime = new Date(uHis.currentTime);
                const ret = (uHis.currentAmount - uHis.beginningAmount) / uHis.beginningAmount;
                const days = (uHis.currentTime - uHis.beginningTime) / (1000 * 3600 * 24);
                uHis.annualizedReturnRate = ret / days * 365;

                uHis.beginningTimeFmt = timeFormat(uHis.beginningTime);
                uHis.annualizedReturnRateFmt = (uHis.annualizedReturnRate * 100).toFixed(2) + '%';
                uHis.beginningAmountFmt = uHis.beginningAmount.toFixed(2);
                uHis.currentAmountFmt = uHis.currentAmount.toFixed(2);

                const endingTime = new Date(uHis.beginningTime);
                endingTime.setDate(endingTime.getDate() + uHis.lockupPeriod);
                uHis.residualLockupPeriod = Math.max(Math.ceil((endingTime - new Date()) / (1000 * 3600 * 24)), 2);
            }
        }
        return data;
    }

    async getChinaBondYieldData (months) {
        console.log(months);
        const dates = this.sampleDates(months).map(t => timeFormat(t));
        const data = await getChinaBondYieldDataRequest(dates);
        console.log(data);
        return data.yields;
    }

    getData () {
        const data = {
            cashData: [],
            monetaryFundData: [],
            fixedDepositData: [],
            fundData: []
        };
        for (let cdata of this.data.cashData) {
            const last = cdata.history[cdata.history.length - 1];
            if (last.amount <= 0) {
                continue;
            }
            const d = {
                name: last.name,
                amount: last.amount,
                amountFmt: last.amountFmt,
                beginningTime: last.beginningTime
            };
            d.id = cdata.id;
            data.cashData.push(d);
        }
        for (let mdata of this.data.monetaryFundData) {
            // filter: holding === true
            const last = mdata.history[mdata.history.length - 1];
            if (last.holding !== true) {
                continue;
            }
            const d = {
                name: last.name,
                beginningAmount: last.beginningAmount,
                beginningTime: last.beginningTime,
                beginningTimeFmt: last.beginningTimeFmt,
                currentAmount: last.currentAmount,
                currentAmountFmt: last.currentAmountFmt,
                currentTime: last.currentTime,
                fastRedemption: last.fastRedemption,
                fastRedemptionFmt: last.fastRedemptionFmt,
                annualizedReturnRate: last.annualizedReturnRate,
                annualizedReturnRateFmt: last.annualizedReturnRateFmt,
                holding: last.holding
            };
            d.id = mdata.id;
            data.monetaryFundData.push(d);
        }
        for (let fdata of this.data.fixedDepositData) {
            // filter: endingTime >= now
            let last = fdata.history[fdata.history.length - 1];
            if (new Date() > last.endingTime) {
                continue;
            }
            const d = {
                name: last.name,
                beginningAmount: last.beginningAmount,
                beginningAmountFmt: last.beginningAmountFmt,
                rate: last.rate,
                rateFmt: last.rateFmt,
                maturity: last.maturity,
                beginningTime: last.beginningTime,
                beginningTimeFmt: last.beginningTimeFmt,
                endingAmount: last.endingAmount,
                endingAmountFmt: last.endingAmountFmt,
                endingTime: last.endingTime,
                endingTimeFmt: last.endingTimeFmt,
                residualMaturaty: last.residualMaturaty
            };
            d.id = fdata.id;
            data.fixedDepositData.push(d);
        }
        for (let udata of this.data.fundData) {
            // filter: holding === true
            const last = udata.history[udata.history.length - 1];
            if (last.holding !== true) {
                continue;
            }
            const d = {
                name: last.name,
                beginningAmount: last.beginningAmount,
                beginningAmountFmt: last.beginningAmountFmt,
                beginningTime: last.beginningTime,
                beginningTimeFmt: last.beginningTimeFmt,
                currentAmount: last.currentAmount,
                currentAmountFmt: last.currentAmountFmt,
                currentTime: last.currentTime,
                lockupPeriod: last.lockupPeriod,
                residualLockupPeriod: last.residualLockupPeriod,
                annualizedReturnRate: last.annualizedReturnRate,
                annualizedReturnRateFmt: last.annualizedReturnRateFmt,
                holding: last.holding
            };
            d.id = udata.id;
            data.fundData.push(d);
        }
        return data;
    }

    download () {
        const json = JSON.stringify(this.json);
        const blob = new Blob([json], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'pantalone.json';
        a.click();
        window.URL.revokeObjectURL(url);
    }

    upload (file, callback) {
        uploadRequest(file, callback);
    }

    async addData (type, data, id) {
        console.log(type)
        console.log(data)
        console.log(id)
        await addDataRequest(type, data, id)
        await this.load()
        this.data = this.prepareData()
    }

    sampleDates (months) {
        let dates = [];
        let currentDate = new Date();

        const interval = Math.ceil(months / 12);
        for (let i = 0; i < months; i += interval) {
            let newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, currentDate.getDate() + 1);
            dates.unshift(newDate);
        }
        return dates;
    }

    getAssetChangeData (months) {
        const dates = this.sampleDates(months);
        const cashData = [];
        const monetaryFundData = [];
        const fixedDepositData = [];
        const fundData = [];

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
                if (d && d.holding && d.currentAmount > 0) {
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

            let fund = 0;
            for (let uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.beginningTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    fund += d.currentAmount;
                }
            }
            fundData.push(fund);
        }
        return {
            time: dates.map(t => timeFormat(t, true)),
            cashData: cashData,
            monetaryFundData: monetaryFundData,
            fixedDepositData: fixedDepositData,
            fundData: fundData
        }
    }

    getAssetDeltaChangeData (assetChangeData) {
        const cashDelta = [0];
        const monetaryFundDelta = [0];
        const fixedDepositDelta = [0];
        const fundDelta = [0];
        const totalDelta = [0];
        for (let i = 1; i < assetChangeData.time.length; i++) {
            cashDelta.push(assetChangeData.cashData[i] - assetChangeData.cashData[i - 1]);
            monetaryFundDelta.push(assetChangeData.monetaryFundData[i] - assetChangeData.monetaryFundData[i - 1]);
            fixedDepositDelta.push(assetChangeData.fixedDepositData[i] - assetChangeData.fixedDepositData[i - 1]);
            fundDelta.push(assetChangeData.fundData[i] - assetChangeData.fundData[i - 1]);
            totalDelta.push(cashDelta[i] + monetaryFundDelta[i] + fixedDepositDelta[i] + fundDelta[i]);
        }
        return {
            time: assetChangeData.time,
            cashDeltaData: cashDelta,
            monetaryFundDeltaData: monetaryFundDelta,
            fixedDepositDeltaData: fixedDepositDelta,
            fundDeltaData: fundDelta,
            totalDeltaData: totalDelta
        }
    }

    getResidualMaturityData () {
        const maturitiyData = [
            { name: "T+0", amount: 0 },
            { name: "T+1", amount: 0 },
            { name: "T+2", amount: 0 },
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
            if (last.residualMaturaty < 0) {
                continue;
            } else if (last.residualMaturaty <= 30) {
                maturitiyData[3].amount += last.beginningAmount;
            } else if (last.residualMaturaty <= 90) {
                maturitiyData[4].amount += last.beginningAmount;
            } else if (last.residualMaturaty <= 180) {
                maturitiyData[5].amount += last.beginningAmount;
            } else if (last.residualMaturaty <= 365) {
                maturitiyData[6].amount += last.beginningAmount;
            } else {
                maturitiyData[7].amount += last.beginningAmount;
            }
        }
        for (let uData of this.data.fundData) {
            const last = uData.history[uData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.residualLockupPeriod <= 0) {
                continue;
            } else if (last.residualLockupPeriod === 2) {
                maturitiyData[2].amount += last.currentAmount;
            } else if (last.residualLockupPeriod <= 30) {
                maturitiyData[3].amount += last.currentAmount;
            } else if (last.residualLockupPeriod <= 90) {
                maturitiyData[4].amount += last.currentAmount;
            } else if (last.residualLockupPeriod <= 180) {
                maturitiyData[5].amount += last.currentAmount;
            } else if (last.residualLockupPeriod <= 365) {
                maturitiyData[6].amount += last.currentAmount;
            } else {
                maturitiyData[7].amount += last.currentAmount;
            }
        }
        maturitiyData.forEach(item => {
            item.value = item.amount;
        });
        return maturitiyData;
    }

    getExpectedReturnData () {
        const expectedReturn = [
            { name: "<1%", amount: 0 },
            { name: "1%-2%", amount: 0 },
            { name: "2%-5%", amount: 0 },
            { name: "5%-10%", amount: 0 },
            { name: ">10%", amount: 0 }
        ]

        for (let cData of this.data.cashData) {
            const last = cData.history[cData.history.length - 1];
            expectedReturn[0].amount += last.amount;
        }
        for (let mData of this.data.monetaryFundData) {
            const last = mData.history[mData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.annualizedReturnRate < 0.01) {
                expectedReturn[0].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.02) {
                expectedReturn[1].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.05) {
                expectedReturn[2].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.1) {
                expectedReturn[3].amount += last.currentAmount;
            } else {
                expectedReturn[4].amount += last.currentAmount;
            }
        }
        for (let fData of this.data.fixedDepositData) {
            const last = fData.history[fData.history.length - 1];
            if (last.residualMaturaty < 0) {
                continue;
            }
            if (last.rate < 0.01) {
                expectedReturn[0].amount += last.beginningAmount;
            } else if (last.rate < 0.02) {
                expectedReturn[1].amount += last.beginningAmount;
            } else if (last.rate < 0.05) {
                expectedReturn[2].amount += last.beginningAmount;
            } else if (last.rate < 0.1) {
                expectedReturn[3].amount += last.beginningAmount;
            } else {
                expectedReturn[4].amount += last.beginningAmount;
            }
        }
        for (let uData of this.data.fundData) {
            const last = uData.history[uData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.annualizedReturnRate < 0.01) {
                expectedReturn[0].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.02) {
                expectedReturn[1].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.05) {
                expectedReturn[2].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.1) {
                expectedReturn[3].amount += last.currentAmount;
            } else {
                expectedReturn[4].amount += last.currentAmount;
            }
        }
        expectedReturn.forEach(item => {
            item.value = item.amount;
        });
        return expectedReturn;
    }

    getLiquidityReturnPositionData () {
        let data = []
        for (let cData of this.data.cashData) {
            const last = cData.history[cData.history.length - 1];
            data.push({
                liquidity: 1,
                return: 0,
                amount: last.amount
            })
        }
        for (let mData of this.data.monetaryFundData) {
            const last = mData.history[mData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.fastRedemption) {
                data.push({
                    liquidity: 1,
                    return: last.annualizedReturnRate,
                    amount: last.currentAmount
                })
            } else {
                data.push({
                    liquidity: 1,
                    return: last.annualizedReturnRate,
                    amount: last.currentAmount
                })
            }
        }
        for (let fData of this.data.fixedDepositData) {
            const last = fData.history[fData.history.length - 1];
            if (last.residualMaturaty <= 0) {
                continue;
            }
            data.push({
                liquidity: last.residualMaturaty,
                return: last.rate,
                amount: last.beginningAmount
            })
        }
        for (let uData of this.data.fundData) {
            const last = uData.history[uData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            data.push({
                liquidity: last.residualLockupPeriod,
                return: last.annualizedReturnRate,
                amount: last.currentAmount
            })
        }
        data = data.sort((a, b) => {
            if (a.liquidity === b.liquidity) {
                return a.return - b.return;
            }
            return a.liquidity - b.liquidity;
        });
        data = data.reduce((acc, cur) => {
            if (acc.length === 0) {
                acc.push(cur);
            } else {
                const last = acc[acc.length - 1];
                if (last.liquidity === cur.liquidity && last.return === cur.return) {
                    last.amount += cur.amount;
                } else {
                    acc.push(cur);
                }
            }
            return acc;
        }, []);

        return {
            data: data.map(d => [d.liquidity, d.return]),
            amount: data.map(d => d.amount)
        };
    }

    getAverageReturnData (months, yields) {
        console.log(yields);

        const dates = this.sampleDates(months);
        const weightedReturn = [];

        for (let date of dates) {
            let weighted = 0;
            let sum = 0;
            for (let mData of this.data.monetaryFundData) {
                const candidate = mData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    weighted += d.currentAmount * d.annualizedReturnRate;
                    sum += d.currentAmount;
                }
            }
            for (let fData of this.data.fixedDepositData) {
                const candidate = fData.history.filter(h => h.beginningTime <= date && h.endingTime >= date);
                const d = candidate[candidate.length - 1];
                if (d && d.beginningAmount > 0) {
                    weighted += d.beginningAmount * d.rate;
                    sum += d.beginningAmount;
                }
            }
            for (let uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.beginningTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    weighted += d.currentAmount * d.annualizedReturnRate;
                    sum += d.currentAmount;
                }
            }
            weightedReturn.push(weighted / sum);
        }
        return {
            time: dates.map(t => timeFormat(t, true)),
            data: weightedReturn,
            yields: yields.map(y => y.yield)
        }
    }

    async getRiskIndicatorData (averageReturn, period, p) {
        const ret = averageReturn.data;
        const yields = averageReturn.yields;

        const excessReturn = ret.map((r, i) => r - yields[i]);

        const meanReturn = statistic.rolling(excessReturn, period, statistic.nanmean);
        const stdReturn = statistic.rolling(excessReturn, period, statistic.nanstd);
        const sharpeRatio = meanReturn.map((m, i) => m / stdReturn[i]);
        const n = statistic.rolling(excessReturn, period, statistic.countNotNaN);

        console.log(excessReturn);
        console.log(meanReturn);
        console.log(stdReturn);
        console.log(sharpeRatio);
        console.log(n)

        // https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf
        const interval = await getNormalIntervalRequest(p);
        console.log(interval);

        const confidence = sharpeRatio.map((v, i) => {
            const right = Math.sqrt((1 + 0.5 * v ** 2) / n[i]);
            return {
                lower: interval.lower * right,
                upper: interval.upper * right
            }
        })

        console.log(confidence);

        return {
            time: averageReturn.time,
            sharpeRatio: sharpeRatio,
            sharpeConfidence: confidence
        }
    }
}

export default Data;