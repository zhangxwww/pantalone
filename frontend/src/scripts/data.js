import statistic from './statistic.js';
import { timeFormat } from './formatter.js';
import { classifyFund, allClasses } from './fundClassifier.js';
import {
    getChinaBondYieldDataRequest,
    getLPRDataRequest,
    loadDataRequest,
    uploadRequest,
    addDataRequest,
    getNormalIntervalRequest,
    getIndexCloseRequest,
    getRefreshedFundNetValueRequest,
} from './requests.js';


function clone (x) {
    return JSON.parse(JSON.stringify(x));
}


export default class Data {
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
            for (let [i, mHis] of mData.history.entries()) {
                mHis.beginningTime = new Date(mHis.beginningTime);
                mHis.currentTime = new Date(mHis.currentTime);

                mHis.beginningReferenceAmount = mHis.beginningAmount;
                mHis.referenceAmount = mHis.currentAmount;
                if (mHis.currency !== 'CNY') {
                    mHis.referenceAmount *= mHis.currencyRate;
                    mHis.beginningReferenceAmount *= mHis.beginningCurrencyRate;
                    // NOTE:
                    // beginningShares is denominated in foreign currency
                    // currentShares is denominated in local currency
                    mHis.beginningShares *= mHis.beginningCurrencyRate;
                }

                mHis.beginningNetValue = mHis.beginningReferenceAmount / mHis.beginningShares;
                mHis.currentNetValue = mHis.referenceAmount / mHis.currentShares;

                if (i === 0) {
                    const ret = (mHis.currentNetValue - mHis.beginningNetValue) / mHis.beginningNetValue;
                    const days = (mHis.currentTime - mHis.beginningTime) / (1000 * 3600 * 24);

                    mHis.annualizedReturnRate = ret / days * 365;
                    mHis.annualizedReturnRate = isNaN(mHis.annualizedReturnRate) ? 0 : mHis.annualizedReturnRate;
                    mHis.latestReturnRate = mHis.annualizedReturnRate;
                    mHis.cumReturnRate = 1;
                } else {
                    let latest = mData.history.slice().reverse().find(e => mHis.currentTime - e.currentTime >= 24 * 3600 * 1000);
                    latest = latest || mData.history[0];
                    const latestSpan = (latest.currentTime - latest.beginningTime) / (1000 * 3600 * 24);
                    const currentRet = (mHis.currentNetValue - latest.currentNetValue) / latest.currentNetValue;
                    const currentSpan = (mHis.currentTime - latest.currentTime) / (1000 * 3600 * 24);

                    if (currentSpan < 1) {
                        mHis.annualizedReturnRate = latest.annualizedReturnRate;
                    } else {
                        mHis.annualizedReturnRate = statistic.averageMean(latest.annualizedReturnRate, currentRet / currentSpan * 365, latestSpan, currentSpan);
                    }
                    mHis.latestReturnRate = currentRet / currentSpan * 365;
                    mHis.cumReturnRate = latest.cumReturnRate * (currentRet + 1);
                }
                mHis.cumReturn = mHis.referenceAmount - mHis.currentShares;


                mHis.referenceAmountFmt = mHis.referenceAmount.toFixed(2);

                mHis.beginningTimeFmt = timeFormat(mHis.beginningTime);
                mHis.annualizedReturnRateFmt = (mHis.annualizedReturnRate * 100).toFixed(2) + '%';
                mHis.latestReturnRateFmt = (mHis.latestReturnRate * 100).toFixed(2) + '%';
                mHis.currentAmountFmt = mHis.currentAmount.toFixed(2);
                mHis.currentSharesFmt = mHis.currentShares.toFixed(2);
                mHis.cumReturnFmt = mHis.cumReturn.toFixed(2);
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
            for (let [i, uHis] of uData.history.entries()) {
                uHis.currentTime = new Date(uHis.currentTime);
                uHis.currentAmount = uHis.currentShares * uHis.currentNetValue;
                uHis.currentDividend = uHis.dividendRatio * uHis.currentShares;
                const latest = uData.history.slice().reverse().find(e => uHis.currentTime - e.currentTime >= 24 * 3600 * 1000);
                if (i === 0 || !latest) {
                    uHis.annualizedReturnRate = 0;
                    uHis.cumInvest = uHis.currentAmount;
                    uHis.cumReturn = 0;
                    uHis.cumDividendRatio = 0;
                    uHis.cumDividend = 0;
                    uHis.cumReturnRate = 1;
                    uHis.latestReturnRate = 0;
                    uHis.averageHoldingCost = uHis.currentNetValue;
                    uHis.cumNetValue = uHis.currentNetValue + uHis.cumDividendRatio;
                    uHis.maxNetValue = uHis.currentNetValue;
                } else {
                    const first = uData.history[0];
                    const firstSpan = (uHis.currentTime - first.currentTime) / (1000 * 3600 * 24);

                    uHis.cumDividendRatio = uHis.dividendRatio + latest.cumDividendRatio;
                    uHis.cumDividend = uHis.currentDividend + latest.cumDividend;

                    const currentRet = (uHis.currentNetValue - latest.currentNetValue + uHis.cumDividendRatio - latest.cumDividendRatio) / (latest.currentNetValue + latest.cumDividendRatio);
                    const currentSpan = (uHis.currentTime - latest.currentTime) / (1000 * 3600 * 24);

                    uHis.cumNetValue = uHis.currentNetValue + uHis.cumDividendRatio;

                    if (uHis.currentShares > latest.currentShares) {
                        uHis.averageHoldingCost = statistic.averageMean(latest.averageHoldingCost, uHis.currentNetValue, latest.currentShares, uHis.currentShares, 'arithmetic');
                    } else {
                        uHis.averageHoldingCost = latest.averageHoldingCost;
                    }

                    uHis.annualizedReturnRate = ((uHis.cumNetValue - uHis.averageHoldingCost) / uHis.averageHoldingCost) / firstSpan * 365;

                    uHis.cumInvest = latest.cumInvest + (uHis.currentShares - latest.currentShares) * uHis.currentNetValue;
                    uHis.cumReturn = uHis.currentAmount - uHis.cumInvest + uHis.cumDividend;
                    uHis.cumReturnRate = latest.cumReturnRate * (currentRet + 1);

                    uHis.latestReturnRate = currentRet / currentSpan * 365;

                    uHis.maxNetValue = Math.max(latest.maxNetValue, uHis.currentNetValue);
                }
                uHis.currentAmountFmt = uHis.currentAmount.toFixed(2);
                uHis.currentSharesFmt = uHis.currentShares.toFixed(2);
                uHis.currentNetValueFmt = uHis.currentNetValue.toFixed(4);

                uHis.cumInvestFmt = uHis.cumInvest.toFixed(2);
                uHis.cumReturnFmt = uHis.cumReturn.toFixed(2);
                uHis.latestReturnRateFmt = (uHis.latestReturnRate * 100).toFixed(2) + '%';
                uHis.cumDividendFmt = uHis.cumDividend.toFixed(2);

                const endingTime = new Date(uHis.currentTime);
                endingTime.setDate(endingTime.getDate() + uHis.lockupPeriod);
                uHis.residualLockupPeriod = Math.max(Math.ceil((endingTime - new Date()) / (1000 * 3600 * 24)), 2);

                uHis.annualizedReturnRateFmt = (uHis.annualizedReturnRate * 100).toFixed(2) + '%';

                uHis.drawdown = (uHis.maxNetValue - uHis.currentNetValue) / uHis.maxNetValue;
                uHis.drawdownFmt = (uHis.drawdown * 100).toFixed(2) + '%';
                uHis.maxDrawdown = Math.max(latest ? latest.maxDrawdown : 0, uHis.drawdown);
                uHis.maxDrawdownFmt = (uHis.maxDrawdown * 100).toFixed(2) + '%';

                uHis.maxCumReturn = Math.max(uHis.cumReturn, latest ? latest.maxCumReturn : 0);
                uHis.returnDrawdown = (uHis.maxCumReturn - uHis.cumReturn) / uHis.maxCumReturn;
                uHis.returnDrawdownFmt = (uHis.returnDrawdown * 100).toFixed(2) + '%';
            }
        }
        console.log(data);
        return data;
    }

    async getChinaBondYieldData (months) {
        console.log(months);
        const dates = this.sampleDates(months).map(t => timeFormat(t));
        const data = await getChinaBondYieldDataRequest(dates);
        console.log(data);
        return data.yields;
    }

    async getLPRData (months) {
        const dates = this.sampleDates(months).map(t => timeFormat(t));
        const data = await getLPRDataRequest(dates);
        console.log(data);
        return data.lpr;
    }

    async getIndexCloseData (months) {
        const dates = this.sampleDates(months).map(t => timeFormat(t));
        const data = await getIndexCloseRequest(dates);
        console.log(data);
        return data.close;
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
                beginningShares: last.beginningShares,
                beginningTime: last.beginningTime,
                beginningTimeFmt: last.beginningTimeFmt,
                currentAmount: last.currentAmount,
                currentAmountFmt: last.currentAmountFmt,
                currentShares: last.currentShares,
                currentSharesFmt: last.currentSharesFmt,
                currentTime: last.currentTime,
                currency: last.currency,
                currencyRate: last.currencyRate,
                beginningCurrencyRate: last.beginningCurrencyRate,
                referenceAmount: last.referenceAmount,
                referenceAmountFmt: last.referenceAmountFmt,
                fastRedemption: last.fastRedemption,
                fastRedemptionFmt: last.fastRedemptionFmt,
                annualizedReturnRate: last.annualizedReturnRate,
                annualizedReturnRateFmt: last.annualizedReturnRateFmt,
                latestReturnRate: last.latestReturnRate,
                latestReturnRateFmt: last.latestReturnRateFmt,
                cumReturn: last.cumReturn,
                cumReturnFmt: last.cumReturnFmt,
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
                symbol: last.symbol,
                currentAmount: last.currentAmount,
                currentAmountFmt: last.currentAmountFmt,
                currentShares: last.currentShares,
                currentSharesFmt: last.currentSharesFmt,
                currentNetValue: last.currentNetValue,
                currentNetValueFmt: last.currentNetValueFmt,
                currentTime: last.currentTime,
                cumInvest: last.cumInvest,
                cumInvestFmt: last.cumInvestFmt,
                cumDividend: last.cumDividend,
                cumDividendFmt: last.cumDividendFmt,
                cumReturn: last.cumReturn,
                cumReturnFmt: last.cumReturnFmt,
                lockupPeriod: last.lockupPeriod,
                residualLockupPeriod: last.residualLockupPeriod,
                annualizedReturnRate: last.annualizedReturnRate,
                annualizedReturnRateFmt: last.annualizedReturnRateFmt,
                latestReturnRate: last.latestReturnRate,
                latestReturnRateFmt: last.latestReturnRateFmt,
                holding: last.holding,
                drawdown: last.drawdownFmt,
                maxDrawdown: last.maxDrawdownFmt,
                returnDrawdown: last.returnDrawdownFmt
            };
            d.id = udata.id;
            data.fundData.push(d);
        }
        return data;
    }

    async refreshFundNetValue (data, symbols) {
        const d = await getRefreshedFundNetValueRequest(symbols);
        console.log(d);
        const latestNetValue = {};
        for (let refreshed of d.refresh) {
            const s = refreshed.symbol;
            const v = refreshed.value;
            latestNetValue[s] = v;
        }
        console.log(latestNetValue);

        let update = false;

        for (let u of data.fundData) {
            const now = new Date();
            const deltaTime = (now - u.currentTime) / (24 * 3600 * 1000)
            const newNetValue = latestNetValue[u.symbol];
            if (newNetValue === u.currentNetValue) {
                continue
            }
            const toBeAdded = {
                name: u.name,
                symbol: u.symbol,
                currentNetValue: newNetValue,
                currentShares: u.currentShares,
                holding: u.holding,
                lockupPeriod: Math.max(u.lockupPeriod - Math.floor(deltaTime), 2),
                dividendRatio: 0
            }
            console.log(toBeAdded);
            await this._addData('fund', toBeAdded, u.id);
            update = true;
        }

        if (update) {
            await this.load();
            this.data = this.prepareData();
        }

        return update;
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

    async _addData (type, data, id) {
        await addDataRequest(type, data, id);
    }

    async addData (type, data, id) {
        console.log(type);
        console.log(data);
        console.log(id);
        await this._addData(type, data, id);
        await this.load();
        this.data = this.prepareData();
    }

    sampleDates (months) {
        let dates = [];
        let currentDate = new Date();

        const interval = 1;
        for (let i = 0; i < months; i += interval) {
            let newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, currentDate.getDate(), 23, 59, 59);
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

        console.log(dates);

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
                // const first = mData.history[0];
                let add = 0;
                // NOTE: I don't know what this is for, just leave it here

                // if (first.beginningTime < date) {
                //     add = first.beginningAmount;
                // }

                const candidate = mData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    add = d.referenceAmount;
                }
                monetaryFund += add;
            }
            monetaryFundData.push(monetaryFund);

            console.log(monetaryFundData.slice());

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
                const candidate = uData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    fund += d.currentAmount;
                }
            }
            fundData.push(fund);
        }
        return {
            time: dates.map(t => timeFormat(t, false)),
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
            { name: "<0%", amount: 0 },
            { name: "0-1%", amount: 0 },
            { name: "1%-2%", amount: 0 },
            { name: "2%-5%", amount: 0 },
            { name: "5%-10%", amount: 0 },
            { name: "10%-20%", amount: 0 },
            { name: ">20%", amount: 0 },
        ]

        for (let cData of this.data.cashData) {
            const last = cData.history[cData.history.length - 1];
            expectedReturn[1].amount += last.amount;
        }
        for (let mData of this.data.monetaryFundData) {
            const last = mData.history[mData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.annualizedReturnRate < 0) {
                expectedReturn[0].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.01) {
                expectedReturn[1].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.02) {
                expectedReturn[2].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.05) {
                expectedReturn[3].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.1) {
                expectedReturn[4].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.2) {
                expectedReturn[5].amount += last.currentAmount;
            } else {
                expectedReturn[6].amount += last.currentAmount;
            }
        }
        for (let fData of this.data.fixedDepositData) {
            const last = fData.history[fData.history.length - 1];
            if (last.residualMaturaty < 0) {
                continue;
            }
            if (last.rate < 0) {
                expectedReturn[0].amount += last.beginningAmount;
            } else if (last.rate < 0.01) {
                expectedReturn[1].amount += last.beginningAmount;
            } else if (last.rate < 0.02) {
                expectedReturn[2].amount += last.beginningAmount;
            } else if (last.rate < 0.05) {
                expectedReturn[3].amount += last.beginningAmount;
            } else if (last.rate < 0.1) {
                expectedReturn[4].amount += last.beginningAmount;
            } else if (last.rate < 0.2) {
                expectedReturn[5].amount += last.beginningAmount;
            } else {
                expectedReturn[6].amount += last.beginningAmount;
            }
        }
        for (let uData of this.data.fundData) {
            const last = uData.history[uData.history.length - 1];
            if (!last.holding) {
                continue;
            }
            if (last.annualizedReturnRate < 0) {
                expectedReturn[0].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.01) {
                expectedReturn[1].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.02) {
                expectedReturn[2].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.05) {
                expectedReturn[3].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.1) {
                expectedReturn[4].amount += last.currentAmount;
            } else if (last.annualizedReturnRate < 0.2) {
                expectedReturn[5].amount += last.currentAmount;
            } else {
                expectedReturn[6].amount += last.currentAmount;
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
            if (last.amount > 0) {
                data.push({
                    liquidity: 1,
                    return: 0,
                    amount: last.amount,
                    name: last.name
                });
            }

        }
        for (let mData of this.data.monetaryFundData) {
            const last = mData.history[mData.history.length - 1];
            if (!last.holding || last.currentAmount <= 0) {
                continue;
            }
            if (last.fastRedemption) {
                data.push({
                    liquidity: 1,
                    return: last.annualizedReturnRate,
                    amount: last.currentAmount,
                    name: last.name
                });
            } else {
                data.push({
                    liquidity: 1,
                    return: last.annualizedReturnRate,
                    amount: last.currentAmount,
                    name: last.name
                });
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
                amount: last.beginningAmount,
                name: last.name
            });
        }
        for (let uData of this.data.fundData) {
            const last = uData.history[uData.history.length - 1];
            if (!last.holding || last.currentAmount <= 0) {
                continue;
            }
            data.push({
                liquidity: last.residualLockupPeriod,
                return: last.annualizedReturnRate,
                amount: last.currentAmount,
                name: last.name
            });
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
                    last.name = `${last.name}、${cur.name}`;
                } else {
                    acc.push(cur);
                }
            }
            return acc;
        }, []);

        return {
            data: data.map(d => [d.liquidity, d.return]),
            amount: data.map(d => d.amount),
            name: data.map(d => d.name)
        };
    }

    getAverageReturnData (months, yields, lpr) {
        console.log(yields);
        console.log(lpr);

        const dates = this.sampleDates(months);
        const weightedReturn = [];
        const latestReturn = [];

        for (let date of dates) {
            let weighted = 0;
            let latest = 0;
            let sum = 0;
            for (let mData of this.data.monetaryFundData) {
                const candidate = mData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    weighted += d.currentAmount * d.annualizedReturnRate;
                    latest += d.currentAmount * d.latestReturnRate;
                    sum += d.currentAmount;
                }
            }
            for (let fData of this.data.fixedDepositData) {
                const candidate = fData.history.filter(h => h.beginningTime <= date && h.endingTime >= date);
                const d = candidate[candidate.length - 1];
                if (d && d.beginningAmount > 0) {
                    weighted += d.beginningAmount * d.rate;
                    latest += d.beginningAmount * d.rate;
                    sum += d.beginningAmount;
                }
            }
            for (let uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    weighted += d.currentAmount * d.annualizedReturnRate;
                    latest += d.currentAmount * d.latestReturnRate;
                    sum += d.currentAmount;
                }
            }
            weightedReturn.push(weighted / sum);
            latestReturn.push(latest / sum);
        }
        return {
            time: dates.map(t => timeFormat(t, false)),
            data: {
                holding: weightedReturn,
                latest: latestReturn
            },
            yields: yields.map(y => y.yield),
            lpr: lpr.map(y => y.rate)
        }
    }

    async getRiskIndicatorData (averageReturn, period, p) {
        const ret = averageReturn.data.holding;
        const yields = averageReturn.yields;

        const excessReturn = ret.map((r, i) => r - yields[i]);

        const meanReturn = statistic.rolling(excessReturn, period, statistic.nanmean);
        const stdReturn = statistic.rolling(excessReturn, period, statistic.nanstd);
        const sharpeRatio = meanReturn.map((m, i) => stdReturn[i] !== 0 ? m / stdReturn[i] : NaN);
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

    async getCumulativeReturnData (months, indexCloseData, assetChangeData) {
        const dates = this.sampleDates(months);
        const cumReturn = [];
        const deltaReturnRate = [Number.NaN];
        const cumReturnRateGeo = [Number.NaN];
        const cumReturnRateAri = [Number.NaN];

        for (let [i, date] of dates.entries()) {
            let cum = 0;
            for (let mData of this.data.monetaryFundData) {
                const candidate = mData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    cum += d.cumReturn;
                }
            }
            for (let fData of this.data.fixedDepositData) {
                const candidate = fData.history.filter(h => h.beginningTime <= date && h.endingTime >= date);
                const d = candidate[candidate.length - 1];
                if (d && d.beginningAmount > 0) {
                    cum += d.beginningAmount * d.rate * (date - d.beginningTime) / (d.endingTime - d.beginningTime);
                }
            }
            for (let uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    cum += d.cumReturn;
                }
            }
            cumReturn.push(cum);
            if (i > 0) {
                const deltaReturn = cumReturn[i] - cumReturn[i - 1];
                const total = assetChangeData.monetaryFundData[i] + assetChangeData.fixedDepositData[i] + assetChangeData.fundData[i];
                deltaReturnRate.push(deltaReturn / total);

                const crrGeo = isNaN(cumReturnRateGeo[i - 1]) ?
                    deltaReturnRate[i] :
                    (cumReturnRateGeo[i - 1] + 1) * (deltaReturnRate[i] + 1) - 1;
                cumReturnRateGeo.push(crrGeo);
                const crrAri = isNaN(cumReturnRateAri[i - 1]) ?
                    deltaReturnRate[i] :
                    cumReturnRateAri[i - 1] + deltaReturnRate[i];
                cumReturnRateAri.push(crrAri);
            }
        }
        console.log(cumReturn);
        console.log(deltaReturnRate);
        console.log(cumReturnRateGeo);

        const first_not_nan_index = cumReturnRateGeo.findIndex(x => !isNaN(x));

        const allIndexCumReturnRate = {
            '000001': null,
            '000012': null
        };
        for (let code of ['000001', '000012']) {
            let indexCumReturn = Array(first_not_nan_index).fill(Number.NaN);
            indexCumReturn.push(0);
            for (let i = first_not_nan_index + 1; i < indexCloseData.length; i++) {
                indexCumReturn.push(indexCloseData[i][code] / indexCloseData[first_not_nan_index][code] - 1);
            }
            allIndexCumReturnRate[code] = indexCumReturn;
        }
        console.log(allIndexCumReturnRate);

        return {
            time: dates.map(t => timeFormat(t, false)),
            cumReturn: {
                geometric: cumReturnRateGeo,
                arithmetic: cumReturnRateAri,
                '000001': allIndexCumReturnRate['000001'],
                '000012': allIndexCumReturnRate['000012']
            }
        }
    }

    getFundClassChangeData (months) {
        const dates = this.sampleDates(months);
        const fundClassChangeData = {};
        for (const cls of allClasses) {
            fundClassChangeData[cls] = Array(dates.length).fill(0);
        }
        for (let [dateIdx, date] of dates.entries()) {
            for (const uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    const cls = classifyFund(d.name);
                    const amount = d.currentAmount;
                    fundClassChangeData[cls][dateIdx] += amount;
                }
            }
        }
        return {
            time: dates.map(t => timeFormat(t, false)),
            data: fundClassChangeData
        };
    }

    getFundClassReturnData (months) {
        const dates = this.sampleDates(months);
        const weighted = {};
        const weights = {};
        for (const cls of allClasses) {
            weighted[cls] = Array(dates.length).fill(0);
            weights[cls] = Array(dates.length).fill(0);
        }
        for (let [dateIdx, date] of dates.entries()) {
            for (const uData of this.data.fundData) {
                const candidate = uData.history.filter(h => h.currentTime <= date);
                const d = candidate[candidate.length - 1];
                if (d && d.holding && d.currentAmount > 0) {
                    const cls = classifyFund(d.name);
                    const amount = d.currentAmount;
                    const returnRate = d.annualizedReturnRate;
                    weighted[cls][dateIdx] += amount * returnRate;
                    weights[cls][dateIdx] += amount;
                }
            }
        }
        const fundClassReturnData = {};
        for (const cls of allClasses) {
            fundClassReturnData[cls] = Array(dates.length).fill(0);
            for (let i = 0; i < dates.length; i++) {
                fundClassReturnData[cls][i] = weighted[cls][i] / weights[cls][i];
            }
        }
        console.log(weighted);
        console.log(weights);
        console.log(fundClassReturnData);

        return {
            time: dates.map(t => timeFormat(t, false)),
            data: fundClassReturnData
        };
    }

    getFundClassRatioChangeData (fundClassChangeData) {
        const ratio = {};
        for (const cls of allClasses) {
            ratio[cls] = Array(fundClassChangeData.time.length).fill(0);
        }
        for (let i = 0; i < fundClassChangeData.time.length; i++) {
            let sum = 0;
            for (const clsData of Object.values(fundClassChangeData.data)) {
                sum += isNaN(clsData[i]) ? 0 : clsData[i];
            }
            for (const [cls, clsData] of Object.entries(fundClassChangeData.data)) {
                ratio[cls][i] = clsData[i] / sum;
            }
        }
        return { time: fundClassChangeData.time, data: ratio };
    }

    getFundClassDrawdownData (fundClassReturnData) {
        const drawdown = {};
        for (const [cls, clsData] of Object.entries(fundClassReturnData.data)) {
            const cumReturn = statistic.cumsum(clsData);
            drawdown[cls] = statistic.drawdown(cumReturn);
        }
        return { time: fundClassReturnData.time, data: drawdown };
    }

    getDrawdownData (cumReturnData) {

        return {
            time: cumReturnData.time,
            drawdownGeometric: statistic.drawdown(cumReturnData.cumReturn.geometric),
            drawdownArithmetic: statistic.drawdown(cumReturnData.cumReturn.arithmetic),
        }
    }

    getStatisdicData () {
        let earlist = new Date();

        const oneYearBefore = new Date();
        oneYearBefore.setFullYear(oneYearBefore.getFullYear() - 1);

        let lastYearAsset = 0;
        let latestAsset = 0;

        let cumReturn = 0;
        let lastYearBeforeCumReturn = 0;

        for (const cData of this.data.cashData) {
            const first = cData.history[0];
            const latest = cData.history[cData.history.length - 1];
            if (first.beginningTime < earlist) {
                earlist = first.beginningTime;
            }
            const lastYearBeforeHistory = cData.history.filter(h => h.beginningTime <= oneYearBefore);
            const lastYearBefore = lastYearBeforeHistory[lastYearBeforeHistory.length - 1];
            if (lastYearBefore && lastYearBefore.amount > 0) {
                lastYearAsset += lastYearBefore.amount;
            }
            if (latest && latest.amount > 0) {
                latestAsset += latest.amount;
            }
        }
        for (const mData of this.data.monetaryFundData) {
            const first = mData.history[0];
            const latest = mData.history[mData.history.length - 1];
            if (first.beginningTime < earlist) {
                earlist = first.beginningTime;
            }
            const lastYearBeforeHistory = mData.history.filter(h => h.currentTime <= oneYearBefore);
            const lastYearBefore = lastYearBeforeHistory[lastYearBeforeHistory.length - 1];
            if (lastYearBefore && lastYearBefore.holding && lastYearBefore.currentAmount > 0) {
                lastYearAsset += lastYearBefore.currentAmount;
            }
            if (latest && latest.holding && latest.currentAmount > 0) {
                latestAsset += latest.currentAmount;
            }
            if (lastYearBefore) {
                lastYearBeforeCumReturn += lastYearBefore.cumReturn;
            }
            if (latest) {
                cumReturn += latest.cumReturn;
                console.log(latest.name, latest.cumReturn);
            }
        }
        for (const fData of this.data.fixedDepositData) {
            const first = fData.history[0];
            const latest = fData.history[fData.history.length - 1];
            if (first.beginningTime < earlist) {
                earlist = first.beginningTime;
            }
            const lastYearBeforeHistory = fData.history.filter(h => h.beginningTime <= oneYearBefore && h.endingTime >= oneYearBefore);
            const lastYearBefore = lastYearBeforeHistory[lastYearBeforeHistory.length - 1];
            if (lastYearBefore && lastYearBefore.beginningAmount > 0) {
                lastYearAsset += lastYearBefore.beginningAmount;
            }
            if (latest && latest.beginningAmount > 0) {
                latestAsset += latest.beginningAmount;
            }
        }
        for (const uData of this.data.fundData) {
            const first = uData.history[0];
            const latest = uData.history[uData.history.length - 1];
            if (first.currentTime < earlist) {
                earlist = first.currentTime;
            }
            const lastYearBeforeHistory = uData.history.filter(h => h.currentTime <= oneYearBefore);
            const lastYearBefore = lastYearBeforeHistory[lastYearBeforeHistory.length - 1];
            if (lastYearBefore && lastYearBefore.holding && lastYearBefore.currentAmount > 0) {
                lastYearAsset += lastYearBefore.currentAmount;
            }
            if (latest && latest.holding && latest.currentAmount > 0) {
                latestAsset += latest.currentAmount;
            }
            if (lastYearBefore) {
                lastYearBeforeCumReturn += lastYearBefore.cumReturn;
            }
            if (latest) {
                cumReturn += latest.cumReturn;
                console.log(latest.name, latest.cumReturn);
            }
        }
        return {
            totalInvestmentDays: Math.ceil((new Date() - earlist) / (1000 * 3600 * 24)),
            lastYearAssetChange: latestAsset - lastYearAsset,
            lastYearReturn: cumReturn - lastYearBeforeCumReturn,
            totalReturn: cumReturn
        }
    }
}
