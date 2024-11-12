<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ page }}</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
        <el-col :span="6" :offset="9">
          <span style="font-size: var(--el-font-size-large); font-weight: bold">{{ page }}</span>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <el-row style="margin-bottom: 10px;">
            <el-col :span="22">
              <span>
                <el-text size="large">时间范围</el-text>
              </span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom: 20px;">
            <el-col :span="22">
              <el-date-picker v-model="dateRange" type="daterange" start-placeholder="开始日期" end-placeholder="结束日期"
                unlink-panels :shortcuts="dateRangeShortCuts" />
            </el-col>
          </el-row>

          <el-row style="margin-bottom: 10px;">
            <el-col :span="22">
              <span>
                <el-text size="large">采样设置</el-text>
              </span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom: 20px;">
            <el-col :span="4" :push="6">
              <el-select v-model="sampleInternal" placeholder="Select" style="width: 90px">
                <el-option label="日" value="daily" />
                <el-option label="周" value="weekly" />
                <el-option label="月" value="monthly" />
                <el-option label="年" value="yearly" />
              </el-select>
            </el-col>
            <el-col :span="4" :push="8">
              <el-select v-model="sampleFunc" placeholder="Select" style="width: 90px">
                <el-option label="期初值" value="open" />
                <el-option label="最大值" value="high" />
                <el-option label="最小值" value="low" />
                <el-option label="期末值" value="close" />
              </el-select>
            </el-col>
          </el-row>

          <el-row style="margin-bottom: 10px;">
            <el-col :span="22">
              <span>
                <el-text size="large">指标选择</el-text>
              </span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom: 20px;">
            <el-col :span="24">
              <el-row v-for="(indicator, index) in indicators" :key="indicator" align="middle"
                style="margin-bottom: 10px;">
                <el-col :span="22"
                  style="text-align: left; padding: 5px; border-radius: 5px; border: 1px #e0e0e0 solid;">
                  <el-space wrap :size="[6, 6]">
                    <el-tag v-for="item in indicator" :key="item.value"
                      :type="item.type === 'indicator' ? 'primary' : item.type === 'operator' ? 'success' : 'info'">
                      {{ item.label }}
                    </el-tag>
                  </el-space>
                </el-col>
                <el-col :span="2">
                  <el-button type="danger" @click="onDeleteIndicator(index)"
                    style="width: 100%; margin-left: 20%; border-radius: 5px; font-size: 12px; font-weight: lighter; ">
                    删除
                  </el-button>
                </el-col>
              </el-row>
              <el-row align="middle" style="margin-bottom: 10px;">
                <el-col :span="22" style="padding: 5px; border-radius: 5px; border: 1px #e0e0e0 dashed;">
                  <el-button @click="onShowDialog" style="width: 100%; border-width: 0px;">
                    添加指标
                  </el-button>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row style="margin-bottom: 20px;">
            <el-col :span="4" :push="6">
              <el-button @click="onQuery" type="primary">
                查询
              </el-button>
            </el-col>
            <el-col :span="4" :push="8">
              <el-button @click="onReset">
                重置
              </el-button>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="16">
          <div id="playground-chart" style="width: 100%; height: 600px;"></div>
        </el-col>
      </el-row>

      <el-dialog v-model="dialogVisible" title="添加指标" width="30%">
        <el-row align="middle" style="margin-bottom: 10px;">
          <el-col :span="4">
            <el-text>选择数据</el-text>
          </el-col>
          <el-col :span="19" :push="1">
            <el-tree-select v-model="selectedIndicatorValue" :data="indicatorMenu" @change="onAddIndicator"
              :render-after-expand="false" :filter-node-method="filterNodeMethod" filterable style="width: 100%">
              <template #default="{ data: { label, children } }">
                <div v-if="children">
                  {{ label }}
                </div>
                <el-tag v-else type="primary" style="height: 17px;">
                  {{ label }}
                </el-tag>
              </template>
            </el-tree-select>
          </el-col>
        </el-row>

        <el-row align="middle" style="margin-bottom: 10px;">
          <el-col :span="4">
            <el-text>选择运算</el-text>
          </el-col>
          <el-col :span="19" :push="1">
            <el-tree-select v-model="selectedOperatorValue" :data="operatorMenu" @change="onAddOperator"
              :render-after-expand="false" :filter-node-method="filterNodeMethod" filterable style="width: 100%">
              <template #default="{ data: { label, children } }">
                <div v-if="children">
                  {{ label }}
                </div>
                <el-tag v-else type="success">
                  {{ label }}
                </el-tag>
              </template>
            </el-tree-select>
          </el-col>
        </el-row>

        <el-row align="middle" style="margin-bottom: 10px;">
          <el-col :span="4">
            <el-text>添加数字</el-text>
          </el-col>
          <el-col :span="19" :push="1">
            <el-input v-model="addedNumber" @keyup.enter="onAddNumber" />
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24"
            style="text-align: left; padding: 5px; border-radius: 5px; border: 1px #e0e0e0 solid; min-height: 35.6px;">
            <el-space wrap :size="[6, 6]">
              <el-tag v-for="item, index in formular" :key="item.value" disable-transitions closable
                @close="onTagClose(index)"
                :type="item.type === 'indicator' ? 'primary' : item.type === 'operator' ? 'success' : 'info'"
                style="margin-right: 10px;">
                {{ item.label }}
              </el-tag>
            </el-space>
          </el-col>
        </el-row>

        <template #footer>
          <el-button @click="onDialogCancel">
            取消
          </el-button>
          <el-button type="primary" @click="onDialogConfirm">
            确认
          </el-button>
        </template>
      </el-dialog>

      <side-chat :page="page" />
    </el-main>
    <el-footer>
      <version-footer />
    </el-footer>
  </el-container>
</template>

<script>
import SideChat from '../components/SideChat.vue';
import VersionFooter from '../components/VersionFooter.vue';
import { getUCPListRequest, getUCPQueryRequest } from '../scripts/requests';
import { parseUCPString, UCPStringToFormula } from '../scripts/protocol/ucp';
import { FOLLOWED_DATA, INSTRUMENT_INDICATOR_TRANSLATION_LONG } from '../scripts/constant';
import { initGraph, drawGeneralLineGraph } from '../scripts/graph';


export default {
  name: 'Dashboard',
  data () {
    return {
      page: '指标实验室',

      dateRange: [],
      sampleInternal: 'daily',
      sampleFunc: 'close',

      indicators: [],

      dialogVisible: false,

      selectedIndicatorValue: null,
      selectedOperatorValue: null,
      addedNumber: null,

      indicatorMenu: [],
      operatorMenu: [
        {
          label: '普通运算符',
          value: 'operation',
          children: [
            {
              label: '+',
              value: 'ucp:operation/plus/plus',
            }, {
              label: '-',
              value: 'ucp:operation/minus/minus',
            }, {
              label: '*',
              value: 'ucp:operation/mul/mul',
            }, {
              label: '/',
              value: 'ucp:operation/div/div',
            }
          ]
        }
      ],
      filterNodeMethod: (value, data) => data.label.includes(value),

      value2label: {},

      formular: [],

      onQuery: async () => {
        const queries = [];
        for (const indicator of this.indicators) {
          let query = [];
          for (const item of indicator) {
            query.push(item.value);
          }
          query = query.join(' ');
          console.log(query);

          queries.push(query);
        }
        let start_date, end_date;
        if (this.dateRange.length === 2) {
          start_date = this.dateRange[0].toISOString().split('T')[0];
          end_date = this.dateRange[1].toISOString().split('T')[0];
        } else {
          start_date = null;
          end_date = null;
        }
        const res = await getUCPQueryRequest(queries, this.sampleInternal, this.sampleFunc, start_date, end_date);
        console.log(res);
        if (res.ucp_query_result.status === 'success') {
          const legend = queries.map(q => UCPStringToFormula(q));
          this.playgroundChart = drawGeneralLineGraph(this.playgroundChart, res.ucp_query_result.value, legend);
        } else {
          this.$message({
            message: '表达式语法错误',
            type: 'error',
            plain: true,
          });
        }
      },

      onReset: () => {
        this.dateRange = '';
        this.indicators.splice(0, this.indicators.length);
      },


      onTagClose: (index) => {
        this.formular.splice(index, 1);
      },

      onShowDialog: () => {
        this.dialogVisible = true;
        this.selectedIndicatorValue = null;
        this.selectedOperatorValue = null;
        this.addedNumber = null;
        this.formular.splice(0, this.formular.length);
      },

      onDeleteIndicator: (index) => {
        this.indicators.splice(index, 1);
      },

      onDialogConfirm: () => {
        if (this.formular.length > 0) {
          this.dialogVisible = false;
          this.indicators.push(JSON.parse(JSON.stringify(this.formular)));
          this.formular.splice(0, this.formular.length);
        }
      },

      onDialogCancel: () => {
        this.dialogVisible = false;
        this.formular.splice(0, this.formular.length);
      },

      onAddIndicator: () => {
        this.formular.push({
          label: this.value2label[this.selectedIndicatorValue],
          value: this.selectedIndicatorValue,
          type: 'indicator'
        });
        this.selectedIndicatorValue = null;
      },

      onAddOperator: () => {
        this.formular.push({
          label: this.value2label[this.selectedOperatorValue],
          value: this.selectedOperatorValue,
          type: 'operator'
        });
        this.selectedOperatorValue = null;
      },

      onAddNumber: () => {
        if (isNaN(parseFloat(this.addedNumber))) {
          this.$message({
            message: '请输入数字',
            type: 'error',
            plain: true,
          });
          return;
        }
        this.formular.push({
          label: this.addedNumber,
          value: `ucp:constant/${this.addedNumber}/${this.addedNumber}`,
          type: 'number'
        });
        this.addedNumber = null;
      },

      dateRangeShortCuts: [
        {
          text: '过去一周',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            return [start, end]
          },
        },
        {
          text: '过去一个月',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            return [start, end]
          },
        },
        {
          text: '过去一年',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
            return [start, end]
          },
        },
        {
          text: '过去三年',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365 * 3)
            return [start, end]
          },
        },
        {
          text: '过去十年',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365 * 10)
            return [start, end]
          },
        },
        {
          text: '当月至今',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setDate(1)
            return [start, end]
          },
        },
        {
          text: '今年至今',
          value: () => {
            const end = new Date()
            const start = new Date()
            start.setMonth(0)
            start.setDate(1)
            return [start, end]
          },
        },
      ],
    }
  },
  async mounted () {
    this.playgroundChart = initGraph('playground-chart');
    this.playgroundChart = drawGeneralLineGraph(this.playgroundChart, [], []);

    const data = await getUCPListRequest();
    const ucpList = data.ucp_list;
    console.log(ucpList);
    const code2ucp = {};
    for (const ucp of ucpList) {
      if (!code2ucp[ucp.code]) {
        code2ucp[ucp.code] = [];
      }
      code2ucp[ucp.code].push(ucp.ucp);
    }
    for (const cat of FOLLOWED_DATA) {
      const children = [];
      for (const content of cat.content) {
        const key = cat.isKLine ? content.code : content.instrument;
        const items = code2ucp[key];
        if (items.length === 1) {
          children.push({
            value: items[0],
            label: content.name,
          });
        } else {
          const childrenchildren = [];
          for (const i of items) {
            childrenchildren.push({
              value: i,
              label: INSTRUMENT_INDICATOR_TRANSLATION_LONG[parseUCPString(i).code],
            });
          }
          children.push({
            value: content.name,
            label: content.name,
            children: childrenchildren
          });
        }
      }
      this.indicatorMenu.push({
        label: cat.category,
        value: cat.category,
        children: children,
      });
    }

    const v2l = (node) => {
      if (node.children) {
        node.children.forEach(v2l);
      } else {
        this.value2label[node.value] = node.label;
      }
    }

    this.indicatorMenu.forEach(v2l);
    this.operatorMenu.forEach(v2l);

    console.log(this.indicatorMenu);
    console.log(this.operatorMenu);
    console.log(this.value2label);
  },

  unmounted () {
    this.playgroundChart.dispose();
  },

  components: {
    SideChat,
    VersionFooter,
  }
}
</script>