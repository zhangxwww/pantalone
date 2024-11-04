<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ page }}</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
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

const INDICATOR_MENU = [
  {
    label: '经济指标',
    value: 'economic',
    children: [{
      value: 'chengzhenrenkoushiyelv',
      label: '城镇人口失业率',
    }, {
      value: 'guominshengchanzongzhi',
      label: '国民生产总值',
    }]
  }, {
    label: '股票指数',
    value: 'stock',
    children: [{
      value: 'hushen300',
      label: '沪深300（月）',
    }]
  }, {
    label: '黄金价格',
    value: 'gold',
    children: [{
      value: 'huangjin9999',
      label: '黄金现货Au9999（月）',
    }]
  }
];

const OPERATOR_MENU = [
  {
    label: '普通运算符',
    value: 'operatoins',
    children: [
      {
        label: '+',
        value: '+',
      }, {
        label: '-',
        value: '-',
      }, {
        label: '*',
        value: '*',
      }, {
        label: '/',
        value: '/',
      }
    ]
  }
];

const VALUE_2_LABEL = {};
function v2l (node) {
  if (node.children) {
    node.children.forEach(v2l);
  } else {
    VALUE_2_LABEL[node.value] = node.label;
  }
}
INDICATOR_MENU.forEach(v2l);
OPERATOR_MENU.forEach(v2l);

export default {
  name: 'Dashboard',
  data () {
    return {
      page: '指标实验室',

      dateRange: '',
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

      indicators: [],

      dialogVisible: false,

      selectedIndicatorValue: null,
      selectedOperatorValue: null,
      addedNumber: null,

      indicatorMenu: INDICATOR_MENU,
      operatorMenu: OPERATOR_MENU,
      filterNodeMethod: (value, data) => data.label.includes(value),

      value2label: VALUE_2_LABEL,

      formular: [],

      onQuery: () => {
        const queries = [];
        for (const indicator of this.indicators) {
          let query = ''
          for (const item of indicator) {
            query += item.value;
          }
          queries.push(query);
        }
        console.log(queries);
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
          value: this.addedNumber,
          type: 'number'
        });
        this.addedNumber = null;
      }
    }
  },
  components: {
    SideChat,
    VersionFooter,
  }
}
</script>