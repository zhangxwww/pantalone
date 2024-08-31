<template>
    <el-tabs type="border-card" style="width: 80%; margin-left: 10%; margin-bottom: 5%">
        <el-tab-pane label="现金">
            <el-table :data="data.cashData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.cash" :key="i" :prop="header.prop" :label="header.label"
                    :width="header.width" :sortable="header.sortable" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'cash')">
                            编辑
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="货币基金"><el-table :data="data.monetaryFundData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.monetaryFund" :key="i" :prop="header.prop"
                    :label="header.label" :width="header.width" :sortable="header.sortable" />

                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'monetary-fund')">
                            编辑
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="定期存款"><el-table :data="data.fixedDepositData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.fixedDeposit" :key="i" :prop="header.prop"
                    :label="header.label" :width="header.width" :sortable="header.sortable" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'fixed-deposit')">
                            编辑
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
        <el-tab-pane label="基金"><el-table :data="data.fundData" table-layout="auto" style="width: 100%">
                <el-table-column v-for="header, i in headers.fund" :key="i" :prop="header.prop" :label="header.label"
                    :width="header.width" :sortable="header.sortable" />
                <el-table-column label="" align="right">
                    <template #default="scope">
                        <el-button size="small" @click="edit(scope.row, 'fund')">
                            编辑
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-tab-pane>
    </el-tabs>
</template>

<script>
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
                        sortable: false
                    },
                    {
                        prop: 'amountFmt',
                        label: '金额',
                        width: '80',
                        sortable: true
                    }
                ],
                monetaryFund: [
                    {
                        prop: 'name',
                        label: '名称',
                        width: '320',
                        sortable: false
                    },
                    {
                        prop: 'beginningTimeFmt',
                        label: '期初时间',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'currentAmountFmt',
                        label: '当期金额',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'currentSharesFmt',
                        label: '累计投入',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'cumReturnFmt',
                        label: '累计收益',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'annualizedReturnRateFmt',
                        label: '年化收益',
                        width: '105',
                        sortable: true
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
                        sortable: false
                    },
                    {
                        prop: 'beginningAmountFmt',
                        label: '期初金额',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'beginningTimeFmt',
                        label: '期初时间',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'rateFmt',
                        label: '利率',
                        width: '80',
                        sortable: true
                    },
                    {
                        prop: 'endingAmountFmt',
                        label: '期末金额',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'endingTimeFmt',
                        label: '期末时间',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'residualMaturaty',
                        label: '剩余期限',
                        width: '105',
                        sortable: true
                    }
                ],
                fund: [
                    {
                        prop: 'name',
                        label: '名称',
                        width: '240',
                        sortable: false
                    },
                    {
                        prop: 'beginningAmountFmt',
                        label: '期初金额',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'beginningTimeFmt',
                        label: '期初时间',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'currentAmountFmt',
                        label: '当期金额',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'annualizedReturnRateFmt',
                        label: '年化收益',
                        width: '105',
                        sortable: true
                    },
                    {
                        prop: 'residualLockupPeriod',
                        label: '剩余锁定期',
                        width: '120',
                        sortable: true
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