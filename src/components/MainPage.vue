<template>
  <el-row>
    <el-col :span="11">
      <div id="main"
           style="width: 750px; height: 300px"></div>
    </el-col>
    <el-col :span="13">
      <el-row>
        <el-dropdown trigger="hover"
                     v-on:command="onAddSelect">
          <el-button type="primary"
                     @click="onAddClick">
            <el-icon>
              <plus />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="1">1</el-dropdown-item>
              <el-dropdown-item command="2">2</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button>
          <el-icon>
            <download />
          </el-icon>
        </el-button>
        <el-button>
          <el-icon>
            <upload />
          </el-icon>
        </el-button>
      </el-row>
      <el-tabs type="border-card">
        <el-tab-pane label="现金">
          <el-table :data="data.cashData"
                    height="500"
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
                           @click="handleEdit(scope.$index, scope.row)">
                  编辑
                </el-button>
                <el-button size="small"
                           type="danger"
                           @click="handleDelete(scope.$index, scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="货币基金"><el-table :data="data.monetaryFundData"
                    height="500"
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
                           @click="handleEdit(scope.$index, scope.row)">
                  编辑
                </el-button>
                <el-button size="small"
                           type="danger"
                           @click="handleDelete(scope.$index, scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="定期存款"><el-table :data="data.fixedDepositData"
                    height="500"
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
                           @click="handleEdit(scope.$index, scope.row)">
                  编辑
                </el-button>
                <el-button size="small"
                           type="danger"
                           @click="handleDelete(scope.$index, scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
import * as echarts from "echarts"
import {
  Plus,
  Download,
  Upload
} from '@element-plus/icons-vue'
import Data from '@/scripts/data.js'


export default {
  name: 'MainPage',
  data () {
    return {
      chart: null,
      record: null,
      data: null,

      handleEdit: (index, row) => {
        console.log(row.id)
      },
      handleDelete: (index, row) => {
        console.log(index, row)
      },
      onAddClick: () => {
        console.log('click add')
      },
      onAddSelect: type => {
        console.log(type)
      },
      headers: {
        cash: [
          {
            prop: 'name',
            label: '账户',
            width: '80',
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
            width: '160',
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
          }
        ],
        fixedDeposit: [
          {
            prop: 'name',
            label: '名称',
            width: '80',
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
        ]
      }
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

    this.chart = echarts.init(document.getElementById('main'))
    this.chart.setOption({
      title: {
        text: 'ECharts 入门示例'
      },
      tooltip: {},
      xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
      },
      yAxis: {},
      series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }]
    })
  },
  unmounted () {
    this.chart.dispose()
  },

}
</script>