<template>
    <el-tabs type="border-card" style="width: 96%; margin-left: 2%; margin-bottom: 5%">
        <el-tab-pane label="现金">
            <el-table :data="data.cashData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.cash" :key="i" :prop="header.prop" :label="header.label"
                    :width="header.width" :sortable="header.sortable" :sort-method="header.sort_method(header.prop)" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'cash')">
                            更新
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="货币基金">
            <el-table :data="data.monetaryFundData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.monetaryFund" :key="i" :prop="header.prop"
                    :label="header.label" :width="header.width" :sortable="header.sortable"
                    :sort-method="header.sort_method(header.prop)" />

                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'monetary-fund')">
                            更新
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="定期存款">
            <el-table :data="data.fixedDepositData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.fixedDeposit" :key="i" :prop="header.prop"
                    :label="header.label" :width="header.width" :sortable="header.sortable"
                    :sort-method="header.sort_method(header.prop)" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'fixed-deposit')">
                            更新
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="基金">
            <el-table :data="data.fundData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.fund" :key="i" :prop="header.prop" :label="header.label"
                    :width="header.width" :sortable="header.sortable" :sort-method="header.sort_method(header.prop)" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'fund')">
                            更新
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
    </el-tabs>
</template>

<script>
function sortByDefault (col) {
    return (a, b) => {
        return a[col] - b[col];
    }
}

// eslint-disable-next-line no-unused-vars
function placeHolder (col) {
    // eslint-disable-next-line no-unused-vars
    return (a, b) => {
        return 0;
    }
}

function sortByFmtFloat (col) {
    return (a, b) => {
        const aa = parseFloat(a[col]);
        const bb = parseFloat(b[col]);
        console.log(a, b, aa, bb, aa - bb);
        return aa - bb;
    }
}

function sortByFmtPercentile (col) {
    return (a, b) => {
        return parseFloat(a[col].replace('%', '')) - parseFloat(b[col].replace('%', ''));
    }
}

export default {
    name: 'TabTable',
    data () {
        return {
            edit: (row, type) => {
                this.$emit('edit', row, type);
            },
            headers: {
                cash: [
                    {
                        prop: 'name',
                        label: '账户',
                        width: '120',
                        sortable: false,
                        sort_method: placeHolder
                    },
                    {
                        prop: 'amountFmt',
                        label: '金额',
                        width: '80',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    }
                ],
                monetaryFund: [
                    {
                        prop: 'name',
                        label: '名称',
                        width: '320',
                        sortable: false,
                        sort_method: placeHolder
                    },
                    {
                        prop: 'beginningTimeFmt',
                        label: '期初时间',
                        width: '105',
                        sortable: true,
                        sort_method: sortByDefault
                    },
                    {
                        prop: 'currentAmountFmt',
                        label: '当期金额',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'currentSharesFmt',
                        label: '累计投入',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'cumReturnFmt',
                        label: '累计收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'annualizedReturnRateFmt',
                        label: '年化收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtPercentile
                    },
                    {
                        prop: 'latestReturnRateFmt',
                        label: '最新收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtPercentile
                    },
                    {
                        prop: 'fastRedemptionFmt',
                        label: '快速赎回',
                        width: '105',
                        sortable: true,
                        sort_method: (a, b) => {
                            return a === b ? 0 : a ? -1 : 1;
                        }
                    }
                ],
                fixedDeposit: [
                    {
                        prop: 'name',
                        label: '名称',
                        width: '240',
                        sortable: false,
                        sort_method: placeHolder
                    },
                    {
                        prop: 'beginningAmountFmt',
                        label: '期初金额',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'beginningTimeFmt',
                        label: '期初时间',
                        width: '105',
                        sortable: true,
                        sort_method: sortByDefault
                    },
                    {
                        prop: 'rateFmt',
                        label: '利率',
                        width: '80',
                        sortable: true,
                        sort_method: sortByDefault
                    },
                    {
                        prop: 'endingAmountFmt',
                        label: '期末金额',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'endingTimeFmt',
                        label: '期末时间',
                        width: '105',
                        sortable: true,
                        sort_method: sortByDefault
                    },
                    {
                        prop: 'residualMaturaty',
                        label: '剩余期限',
                        width: '105',
                        sortable: true,
                        sort_method: sortByDefault
                    }
                ],
                fund: [
                    {
                        prop: 'name',
                        label: '名称',
                        width: '280',
                        sortable: false,
                        sort_method: placeHolder
                    },
                    {
                        prop: 'symbol',
                        label: '代码',
                        width: '80',
                        sortable: false,
                        sort_method: placeHolder
                    },
                    {
                        prop: 'currentAmountFmt',
                        label: '当期金额',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'currentSharesFmt',
                        label: '当期份额',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'currentNetValueFmt',
                        label: '当前净值',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'cumDividendFmt',
                        label: '累计分红',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'cumInvestFmt',
                        label: '累计投入',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'cumReturnFmt',
                        label: '累计收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtFloat
                    },
                    {
                        prop: 'annualizedReturnRateFmt',
                        label: '年化收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtPercentile
                    },
                    {
                        prop: 'latestReturnRateFmt',
                        label: '最新收益',
                        width: '105',
                        sortable: true,
                        sort_method: sortByFmtPercentile
                    },
                    {
                        prop: 'residualLockupPeriod',
                        label: '剩余锁定期',
                        width: '120',
                        sortable: true,
                        sort_method: sortByDefault
                    }
                ]
            },
        }
    },
    props: {
        data: Object
    }
}
</script>