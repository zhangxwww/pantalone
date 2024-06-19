<template>
  <el-row style="margin-top: 60px">
    <el-col :span="12">
      <div id="asset-change-line-graph"
           style="width: 100%; height: 300px"></div>
    </el-col>
    <el-col :span="12">
      <div id="average-return-line-graph"
           style="width: 100%; height: 300px"></div>
    </el-col>
  </el-row>
  <el-row justify="center">
    <el-radio-group v-model="drawMonths"
                    @change="draw">
      <el-radio-button v-for="radio in drawMonthsRadio"
                       :key="radio.value"
                       :label="radio.label"
                       :value="radio.value" />
    </el-radio-group>
  </el-row>
  <el-row style="margin-top: 60px">
    <el-col :span="12">
      <div id="liquidity-return-position-scatter-graph"
           style="width: 100%; height: 300px"></div>
    </el-col>
    <el-col :span="6">
      <div id="residual-maturity-pie-graph"
           style="width: 100%00px; height: 300px"></div>
    </el-col>
    <el-col :span="6">
      <div id="expected-return-pie-graph"
           style="width: 100%; height: 300px"></div>
    </el-col>
  </el-row>
  <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
    <el-col :span="6"
            :offset="9">
      <span style="font-size: var(--el-font-size-large); font-weight: bold">项目明细</span>
    </el-col>
    <el-col :span="1"
            :offset="5">
      <el-dropdown trigger="hover"
                   v-on:command="onAddSelect">
        <el-button type="primary">
          <el-icon>
            <plus />
          </el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="menu in dropdownMenus"
                              :key="menu.command"
                              :command="menu.command">
              {{ menu.label }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>

    <el-col :span="1"
            style="margin-left: 10px">
      <el-button @click="onDownload">
        <el-icon>
          <download />
        </el-icon>
      </el-button>
    </el-col>

    <el-col :span="1"
            style="margin-left: 10px">
      <el-upload ref="upload"
                 :on-change="onUpload"
                 :auto-upload="false"
                 :show-file-list="false"
                 :limit="1">
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
    <el-tabs type="border-card"
             style="width: 70%; margin-left: 15%; margin-bottom: 5%">
      <el-tab-pane label="现金">
        <el-table :data="data.cashData"
                  table-layout="auto"
                  style="width: 100%">
          <el-table-column v-for="header, i in headers.cash"
                           :key="i"
                           :prop="header.prop"
                           :label="header.label"
                           :width="header.width"
                           :sortable="header.sortable" />
          <el-table-column label=""
                           align="right">
            <template #default="scope">
              <el-button size="small"
                         @click="handleEdit(scope.row, 'cash')">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="货币基金"><el-table :data="data.monetaryFundData"
                  table-layout="auto"
                  style="width: 100%">
          <el-table-column v-for="header, i in headers.monetaryFund"
                           :key="i"
                           :prop="header.prop"
                           :label="header.label"
                           :width="header.width"
                           :sortable="header.sortable" />

          <el-table-column label=""
                           align="right">
            <template #default="scope">
              <el-button size="small"
                         @click="handleEdit(scope.row, 'monetary-fund')">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="定期存款"><el-table :data="data.fixedDepositData"
                  table-layout="auto"
                  style="width: 100%">
          <el-table-column v-for="header, i in headers.fixedDeposit"
                           :key="i"
                           :prop="header.prop"
                           :label="header.label"
                           :width="header.width"
                           :sortable="header.sortable" />
          <el-table-column label=""
                           align="right">
            <template #default="scope">
              <el-button size="small"
                         @click="handleEdit(scope.row, 'fixed-deposit')">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="基金"><el-table :data="data.fundData"
                  table-layout="auto"
                  style="width: 100%">
          <el-table-column v-for="header, i in headers.fund"
                           :key="i"
                           :prop="header.prop"
                           :label="header.label"
                           :width="header.width"
                           :sortable="header.sortable" />
          <el-table-column label=""
                           align="right">
            <template #default="scope">
              <el-button size="small"
                         @click="handleEdit(scope.row, 'fund')">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-row>

  <el-dialog v-model="showAddCashDialog"
             title="添加现金项目"
             width="300px">
    <el-form :model="addCashForm"
             ref="addCashForm"
             :rules="cashRules">
      <el-form-item label="账户"
                    prop="name">
        <el-input v-model="addCashForm.name"></el-input>
      </el-form-item>
      <el-form-item label="金额"
                    prop="amount">
        <el-input v-model="addCashForm.amount"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancelAdd('cash')">取消</el-button>
        <el-button type="primary"
                   @click="onConfirmAdd('cash')">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="showAddMonetaryFundDialog"
             title="添加货币基金项目"
             width="300px">
    <el-form :model="addMonetaryFundForm"
             ref="addMonetaryFundForm"
             :rules="monetaryFundRules">
      <el-form-item label="名称"
                    prop="name">
        <el-input v-model="addMonetaryFundForm.name"></el-input>
      </el-form-item>
      <el-form-item label="期初金额"
                    prop="beginningAmount">
        <el-input v-model="addMonetaryFundForm.beginningAmount"></el-input>
      </el-form-item>
      <el-form-item label="期初时间"
                    prop="beginningTime">
        <el-date-picker v-model="addMonetaryFundForm.beginningTime"
                        type="date"
                        placeholder="选择日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="当期金额"
                    prop="currentAmount">
        <el-input v-model="addMonetaryFundForm.currentAmount"></el-input>
      </el-form-item>
      <el-form-item label="快速赎回"
                    prop="fastRedemption">
        <el-switch v-model="addMonetaryFundForm.fastRedemption"></el-switch>
      </el-form-item>
      <el-form-item label="当前持有"
                    prop="holding">
        <el-switch v-model="addMonetaryFundForm.holding"></el-switch>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancelAdd('monetary-fund')">取消</el-button>
        <el-button type="primary"
                   @click="onConfirmAdd('monetary-fund')">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="showAddFixedDepositDialog"
             title="添加定期存款项目"
             width="300px">
    <el-form :model="addFixedDepositForm"
             :rules="fixedDepositRules"
             ref="addFixedDepositForm">
      <el-form-item label="名称"
                    prop="name">
        <el-input v-model="addFixedDepositForm.name"></el-input>
      </el-form-item>
      <el-form-item label="期初金额"
                    prop="beginningAmount">
        <el-input v-model="addFixedDepositForm.beginningAmount"></el-input>
      </el-form-item>
      <el-form-item label="期初时间"
                    prop="beginningTime">
        <el-date-picker v-model="addFixedDepositForm.beginningTime"
                        type="date"
                        placeholder="选择日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="利率"
                    prop="rate">
        <el-input v-model="addFixedDepositForm.rate"></el-input>
      </el-form-item>
      <el-form-item label="期限"
                    prop="maturity">
        <el-input v-model.number="addFixedDepositForm.maturity"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancelAdd('fixed-deposit')">取消</el-button>
        <el-button type="primary"
                   @click="onConfirmAdd('fixed-deposit')">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<script>
import { Plus, Download, Upload } from '@element-plus/icons-vue'
import Data from '@/scripts/data.js'
import { drawAssetChangeLineGraph } from '@/scripts/graph.js'
import { drawResidualMaturityPieGraph } from '@/scripts/graph.js'
import { drawExpectedReturnPieGraph } from '@/scripts/graph.js'
import { drawLiquidityReturnPositionScatterGraph } from '@/scripts/graph.js'
import { drawAverageReturnLineGraph } from '@/scripts/graph.js'
import storage from '@/scripts/storage.js'
import { isNumberValidator } from '@/scripts/validator.js'

export default {
  name: 'MainPage',
  data () {
    return {
      record: null,
      data: null,

      showAddCashDialog: false,
      showAddMonetaryFundDialog: false,
      showAddFixedDepositDialog: false,

      editId: null,
      drawMonths: 12,

      addCashForm: {
        name: '',
        amount: 0
      },
      addMonetaryFundForm: {
        name: '',
        beginningAmount: 0,
        beginningTime: '',
        currentAmount: 0,
        fastRedemption: false,
        holding: true
      },
      addFixedDepositForm: {
        name: '',
        beginningAmount: 0,
        beginningTime: '',
        rate: 0,
        maturity: 0
      },

      handleEdit: (row, type) => {
        this.editId = row.id

        if (type === 'cash') {
          this.addCashForm.name = row.name
          this.addCashForm.amount = row.amount
          this.showAddCashDialog = true
        } else if (type === 'monetary-fund') {
          this.addMonetaryFundForm.name = row.name
          this.addMonetaryFundForm.beginningAmount = row.beginningAmount
          this.addMonetaryFundForm.beginningTime = row.beginningTime
          this.addMonetaryFundForm.currentAmount = row.currentAmount
          this.addMonetaryFundForm.fastRedemption = row.fastRedemption
          this.addMonetaryFundForm.holding = row.holding
          this.showAddMonetaryFundDialog = true
        } else if (type === 'fixed-deposit') {
          this.addFixedDepositForm.name = row.name
          this.addFixedDepositForm.beginningAmount = row.beginningAmount
          this.addFixedDepositForm.beginningTime = row.beginningTime
          this.addFixedDepositForm.rate = row.rate
          this.addFixedDepositForm.maturity = row.maturity
          this.showAddFixedDepositDialog = true
        }
      },
      onAddSelect: type => {
        switch (type) {
          case 'cash':
            this.showAddCashDialog = true
            break
          case 'monetary-fund':
            this.showAddMonetaryFundDialog = true
            break
          case 'fixed-deposit':
            this.showAddFixedDepositDialog = true
            break
        }
      },
      onCancelAdd: (type) => {
        switch (type) {
          case 'cash':
            this.showAddCashDialog = false
            this.$refs['addCashForm'].resetFields()
            break
          case 'monetary-fund':
            this.showAddMonetaryFundDialog = false
            this.$refs['addMonetaryFundForm'].resetFields()
            break
          case 'fixed-deposit':
            this.showAddFixedDepositDialog = false
            this.$refs['addFixedDepositForm'].resetFields()
            break
        }
      },
      addCashData: () => {
        this.record.addData('cash', {
          name: this.addCashForm.name,
          amount: this.addCashForm.amount
        }, this.editId)
      },
      addMonetaryFundData: () => {
        this.record.addData('monetaryFund', {
          name: this.addMonetaryFundForm.name,
          beginningAmount: this.addMonetaryFundForm.beginningAmount,
          beginningTime: this.addMonetaryFundForm.beginningTime,
          currentAmount: this.addMonetaryFundForm.currentAmount,
          fastRedemption: this.addMonetaryFundForm.fastRedemption,
          holding: this.addMonetaryFundForm.holding
        }, this.editId)
      },
      addFixedDepositData: () => {
        this.record.addData('fixedDeposit', {
          name: this.addFixedDepositForm.name,
          beginningAmount: this.addFixedDepositForm.beginningAmount,
          beginningTime: this.addFixedDepositForm.beginningTime,
          rate: this.addFixedDepositForm.rate,
          maturity: this.addFixedDepositForm.maturity
        }, this.editId)
      },
      onConfirmAdd: (type) => {
        switch (type) {
          case 'cash':
            this.$refs['addCashForm'].validate((valid) => {
              if (valid) {
                this.showAddCashDialog = false
                this.addCashData()
                this.data = this.record.getData()
                this.draw()
                this.$refs['addCashForm'].resetFields()
                this.editId = null
              }
            })
            break
          case 'monetary-fund':
            this.$refs['addMonetaryFundForm'].validate((valid) => {
              if (valid) {
                this.showAddMonetaryFundDialog = false
                this.addMonetaryFundData()
                this.data = this.record.getData()
                this.draw()
                this.$refs['addMonetaryFundForm'].resetFields()
                this.editId = null
              }
            })
            break
          case 'fixed-deposit':
            this.$refs['addFixedDepositForm'].validate((valid) => {
              if (valid) {
                this.showAddFixedDepositDialog = false
                this.addFixedDepositData()
                this.data = this.record.getData()
                this.draw()
                this.$refs['addFixedDepositForm'].resetFields()
                this.editId = null
              }
            })
            break
        }
      },
      onDownload: () => {
        storage.download();
      },
      onUpload: (file) => {
        storage.upload(file);
      },
      draw: () => {
        const assetChange = this.record.getAssetChangeData(this.drawMonths)
        this.assetChangeLineGraph = drawAssetChangeLineGraph('asset-change-line-graph', assetChange)

        const residualMaturaty = this.record.getResidualMaturityData()
        this.residualMaturatyPieGraph = drawResidualMaturityPieGraph('residual-maturity-pie-graph', residualMaturaty)

        const expectedReturn = this.record.getExpectedReturnData()
        this.expectedReturnPieGraph = drawExpectedReturnPieGraph('expected-return-pie-graph', expectedReturn)

        const liquidityReturnPosition = this.record.getLiquidityReturnPositionData()
        this.liquidityReturnPositionScatterGraph = drawLiquidityReturnPositionScatterGraph('liquidity-return-position-scatter-graph', liquidityReturnPosition)

        const averageReturn = this.record.getAverageReturnData(this.drawMonths)
        this.averageReturnLineGraph = drawAverageReturnLineGraph('average-return-line-graph', averageReturn)
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
        }
      ],
      cashRules: {
        name: [
          { required: true, message: '请输入账户名称', trigger: 'blur' }
        ],
        amount: [
          { required: true, message: '请输入金额', trigger: 'blur' },
          {
            message: '金额必须为数字值', trigger: 'blur', validator: isNumberValidator
          }
        ]
      },
      monetaryFundRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        beginningAmount: [
          { required: true, message: '请输入期初金额', trigger: 'blur' },
          {
            message: '期初金额必须为数字值', trigger: 'blur', validator: isNumberValidator
          }
        ],
        beginningTime: [
          { required: true, message: '请选择期初时间', trigger: 'blur' }
        ],
        currentAmount: [
          { required: true, message: '请输入当期金额', trigger: 'blur' },
          {
            message: '当期金额必须为数字值', trigger: 'blur', validator: isNumberValidator
          }
        ]
      },
      fixedDepositRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        beginningAmount: [
          { required: true, message: '请输入期初金额', trigger: 'blur' },
          {
            message: '期初金额必须为数字值', trigger: 'blur', validator: isNumberValidator
          }
        ],
        beginningTime: [
          { required: true, message: '请选择期初时间', trigger: 'blur' }
        ],
        rate: [
          { required: true, message: '请输入利率', trigger: 'blur' },
          {
            message: '利率必须为数字值', trigger: 'blur', validator: isNumberValidator
          }
        ],
        maturity: [
          { required: true, message: '请输入期限', trigger: 'blur' },
          {
            message: '期限必须为数字值', trigger: 'blur', type: 'number'
          }
        ]
      },
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
    Upload
  },

  beforeMount () {
    this.record = new Data()
    this.data = this.record.getData()
  },

  mounted () {
    this.draw();
  },
  unmounted () {
    this.assetChangeLineGraph.dispose()
    this.residualMaturatyPieGraph.dispose()
    this.expectedReturnPieGraph.dispose()
    this.liquidityReturnPositionScatterGraph.dispose()
    this.averageReturnLineGraph.dispose()
  },

}
</script>