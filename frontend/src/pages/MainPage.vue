<template>
    <div>
        <el-row style="margin-top: 60px">
            <el-col :span="12">
                <div id="asset-change-line-graph" style="width: 100%; height: 300px"></div>
            </el-col>
            <el-col :span="12">
                <div id="average-return-line-graph" style="width: 100%; height: 300px"></div>
            </el-col>
        </el-row>
        <el-row style="margin-top: 60px">
            <el-col :span="12">
                <div id="asset-delta-change-bar-graph" style="width: 100%; height: 300px"></div>
            </el-col>
        </el-row>
        <el-row justify="center">
            <el-radio-group v-model="drawMonths" @change="draw">
                <el-radio-button v-for="radio in drawMonthsRadio" :key="radio.value" :label="radio.label"
                    :value="radio.value" />
            </el-radio-group>
        </el-row>
        <el-row style="margin-top: 60px">
            <el-col :span="12">
                <div id="liquidity-return-position-scatter-graph" style="width: 100%; height: 300px"></div>
            </el-col>
            <el-col :span="6">
                <div id="residual-maturity-pie-graph" style="width: 100%00px; height: 300px"></div>
            </el-col>
            <el-col :span="6">
                <div id="expected-return-pie-graph" style="width: 100%; height: 300px"></div>
            </el-col>
        </el-row>
        <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
            <el-col :span="6" :offset="9">
                <span style="font-size: var(--el-font-size-large); font-weight: bold">项目明细</span>
            </el-col>
            <el-col :span="1" :offset="5">
                <el-dropdown trigger="hover" v-on:command="onAddSelect">
                    <el-button type="primary">
                        <el-icon>
                            <plus />
                        </el-icon>
                    </el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item v-for="menu in dropdownMenus" :key="menu.command" :command="menu.command">
                                {{ menu.label }}
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-col>

            <el-col :span="1" style="margin-left: 10px">
                <el-button @click="onDownload">
                    <el-icon>
                        <download />
                    </el-icon>
                </el-button>
            </el-col>

            <el-col :span="1" style="margin-left: 10px">
                <el-upload ref="upload" :on-change="onUpload" :auto-upload="false" :show-file-list="false" :limit="1">
                    <template #trigger>
                        <el-button>
                            <el-icon>
                                <upload />
                            </el-icon>
                        </el-button>
                    </template>
                </el-upload>
            </el-col>
        </el-row>
        <el-row>
            <tab-table :data="data" @edit="handleEdit"></tab-table>
        </el-row>

        <add-cash-dialog ref="addCashDialog" @add="onAddData"></add-cash-dialog>

        <add-monetary-dialog ref="addMonetaryDialog" @add="onAddData"></add-monetary-dialog>

        <add-fixed-dialog ref="addFixedDialog" @add="onAddData"></add-fixed-dialog>

        <add-fund-dialog ref="addFundDialog" @add="onAddData"></add-fund-dialog>
    </div>
</template>

<script>
import { Plus, Download, Upload } from '@element-plus/icons-vue'
import Data from '@/scripts/data.js'
import {
    drawAssetChangeLineGraph,
    drawResidualMaturityPieGraph,
    drawExpectedReturnPieGraph,
    drawLiquidityReturnPositionScatterGraph,
    drawAverageReturnLineGraph,
    drawAssetDeltaChangeBarGraph,

    drawEmptyAssetChangeLineGraph,
    drawEmptyAssetDeltaChangeBarGraph,
    drawEmptyResidualMaturityPieGraph,
    drawEmptyExpectedReturnPieGraph,
    drawEmptyLiquidityReturnPositionScatterGraph,
    drawEmptyAverageReturnLineGraph
} from '@/scripts/graph.js'

import AddCashDialog from '@/components/dialogs/AddCashDialog'
import AddMonetaryDialog from '@/components/dialogs/AddMonetaryDialog'
import AddFixedDialog from '@/components/dialogs/AddFixedDialog.vue'
import AddFundDialog from '@/components/dialogs/AddFundDialog.vue'
import TabTable from '@/components/TabTable.vue'


export default {
    name: 'MainPage',
    data () {
        return {
            record: null,
            data: {
                cashData: [],
                monetaryFundData: [],
                fixedDepositData: [],
                fundData: []
            },

            editId: null,
            drawMonths: 12,

            handleEdit: (row, type) => {
                this.editId = row.id

                if (type === 'cash') {
                    this.$refs.addCashDialog.edit(row)
                } else if (type === 'monetary-fund') {
                    this.$refs.addMonetaryDialog.edit(row)
                } else if (type === 'fixed-deposit') {
                    this.$refs.addFixedDialog.edit(row)
                } else if (type === 'fund') {
                    this.$refs.addFundDialog.edit(row)
                }
            },
            onAddSelect: type => {
                this.editId = null

                switch (type) {
                    case 'cash':
                        this.$refs.addCashDialog.show()
                        break
                    case 'monetary-fund':
                        this.$refs.addMonetaryDialog.show()
                        break
                    case 'fixed-deposit':
                        this.$refs.addFixedDialog.show()
                        break
                    case 'fund':
                        this.$refs.addFundDialog.show()
                        break
                }
            },
            addCashData: async (form) => {
                await this.record.addData('cash', {
                    name: form.name,
                    amount: form.amount
                }, this.editId)
            },
            addMonetaryFundData: async (form) => {
                await this.record.addData('monetary-fund', {
                    name: form.name,
                    beginningAmount: form.beginningAmount,
                    beginningTime: form.beginningTime,
                    currentAmount: form.currentAmount,
                    fastRedemption: form.fastRedemption,
                    holding: form.holding
                }, this.editId)
            },
            addFixedDepositData: async (form) => {
                await this.record.addData('fixed-deposit', {
                    name: form.name,
                    beginningAmount: form.beginningAmount,
                    beginningTime: form.beginningTime,
                    rate: form.rate,
                    maturity: form.maturity
                }, this.editId)
            },
            addFundData: async (form) => {
                await this.record.addData('fund', {
                    name: form.name,
                    beginningAmount: form.beginningAmount,
                    beginningTime: form.beginningTime,
                    currentAmount: form.currentAmount,
                    lockupPeriod: form.lockupPeriod,
                    holding: form.holding
                }, this.editId)
            },
            onAddData: async (form, type) => {
                switch (type) {
                    case 'cash':
                        await this.addCashData(form)
                        break
                    case 'monetary-fund':
                        await this.addMonetaryFundData(form)
                        break
                    case 'fixed-deposit':
                        await this.addFixedDepositData(form)
                        break
                    case 'fund':
                        await this.addFundData(form)
                        break
                }
                this.data = this.record.getData()
                this.draw()
                this.editId = null
            },

            onDownload: () => {
                this.record.download();
            },
            onUpload: (file) => {
                this.record.upload(file, () => { location.reload(); });
            },
            drawEmpty: () => {
                const dates = this.record.sampleDates(this.drawMonths);
                this.assetChangeLineGraph = drawEmptyAssetChangeLineGraph('asset-change-line-graph', dates);
                this.assetDeltaChangeBarGraph = drawEmptyAssetDeltaChangeBarGraph('asset-delta-change-bar-graph', dates);
                this.residualMaturatyPieGraph = drawEmptyResidualMaturityPieGraph('residual-maturity-pie-graph');
                this.expectedReturnPieGraph = drawEmptyExpectedReturnPieGraph('expected-return-pie-graph');
                this.liquidityReturnPositionScatterGraph = drawEmptyLiquidityReturnPositionScatterGraph('liquidity-return-position-scatter-graph');
                this.averageReturnLineGraph = drawEmptyAverageReturnLineGraph('average-return-line-graph', dates);
            },
            draw: () => {
                const assetChange = this.record.getAssetChangeData(this.drawMonths)
                this.assetChangeLineGraph = drawAssetChangeLineGraph('asset-change-line-graph', assetChange)

                const assetDeltaChange = this.record.getAssetDeltaChangeData(assetChange)
                this.assetDeltaChangeBarGraph = drawAssetDeltaChangeBarGraph('asset-delta-change-bar-graph', assetDeltaChange)

                const residualMaturaty = this.record.getResidualMaturityData()
                this.residualMaturatyPieGraph = drawResidualMaturityPieGraph('residual-maturity-pie-graph', residualMaturaty)

                const expectedReturn = this.record.getExpectedReturnData()
                this.expectedReturnPieGraph = drawExpectedReturnPieGraph('expected-return-pie-graph', expectedReturn)

                const liquidityReturnPosition = this.record.getLiquidityReturnPositionData()
                this.liquidityReturnPositionScatterGraph = drawLiquidityReturnPositionScatterGraph('liquidity-return-position-scatter-graph', liquidityReturnPosition)

                const averageReturn = this.record.getAverageReturnData(this.drawMonths)
                this.averageReturnLineGraph = drawAverageReturnLineGraph('average-return-line-graph', averageReturn)
            },

            dropdownMenus: [
                {
                    command: 'cash',
                    label: '现金'
                },
                {
                    command: 'monetary-fund',
                    label: '货币基金'
                },
                {
                    command: 'fixed-deposit',
                    label: '定期存款'
                },
                {
                    command: 'fund',
                    label: '基金'
                }
            ],

            drawMonthsRadio: [
                {
                    label: '过去12个月',
                    value: 12
                },
                {
                    label: '过去24个月',
                    value: 24
                },
                {
                    label: '过去36个月',
                    value: 36
                }
            ]
        }
    },
    components: {
        Plus,
        Download,
        Upload,
        AddCashDialog,
        AddMonetaryDialog,
        AddFixedDialog,
        AddFundDialog,
        TabTable,
    },

    async mounted () {
        this.record = new Data()
        this.drawEmpty()
        await this.record.load()
        this.data = this.record.getData()
        // this.draw();
    },
    unmounted () {
        this.assetChangeLineGraph.dispose()
        this.residualMaturatyPieGraph.dispose()
        this.expectedReturnPieGraph.dispose()
        this.liquidityReturnPositionScatterGraph.dispose()
        this.averageReturnLineGraph.dispose()
        this.assetDeltaChangeBarGraph.dispose()
    },

}
</script>