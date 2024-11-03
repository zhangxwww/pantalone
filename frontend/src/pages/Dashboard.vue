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
              <el-row v-for="indicator in indicators" :key="indicator" align="middle" style="margin-bottom: 10px;">
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
                  <el-button round size="small" style="width: 5px; border-color: red; border-width: 1px;">
                    <el-icon color="red">
                      <minus />
                    </el-icon>
                  </el-button>
                </el-col>
              </el-row>
              <el-row align="middle" style="margin-bottom: 10px;">
                <el-col :span="22" style="padding: 5px; border-radius: 5px; border: 1px #e0e0e0 dashed;">
                  <el-button style="width: 100%; border-width: 0px;">
                    添加指标
                  </el-button>
                </el-col>
              </el-row>
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
          <el-col :span="17" :push="1">
            <el-tree-select v-model="selectedIndicatorValue" :data="indicatorMenu" :render-after-expand="false"
              :filter-node-method="filterNodeMethod" filterable style="width: 100%">
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
          <el-col :span="2" :push="1">
            <el-button type="primary" round size="small" style="width: 5px">
              <el-icon :size="8" color="white">
                <plus />
              </el-icon>
            </el-button>
          </el-col>
        </el-row>

        <el-row align="middle" style="margin-bottom: 10px;">
          <el-col :span="4">
            <el-text>选择运算</el-text>
          </el-col>
          <el-col :span="17" :push="1">
            <el-tree-select v-model="selectedOperatorValue" :data="operatorMenu" :render-after-expand="false"
              :filter-node-method="filterNodeMethod" filterable style="width: 100%">
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
          <el-col :span="2" :push="1">
            <el-button type="primary" round size="small" style="width: 5px">
              <el-icon :size="8" color="white">
                <plus />
              </el-icon>
            </el-button>
          </el-col>
        </el-row>

        <el-row align="middle" style="margin-bottom: 10px;">
          <el-col :span="4">
            <el-text>添加数字</el-text>
          </el-col>
          <el-col :span="17" :push="1">
            <el-input v-model="addedNumber" />
          </el-col>
          <el-col :span="2" :push="1">
            <el-button type="primary" round size="small" style="width: 5px">
              <el-icon :size="8" color="white">
                <plus />
              </el-icon>
            </el-button>
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
          <el-button @click="dialogVisible = false">
            Cancel
          </el-button>
          <el-button type="primary" @click="dialogVisible = false; console.log(selectedIndicatorValue)">
            Confirm
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
import { Minus, Plus } from '@element-plus/icons-vue';


export default {
  name: 'Dashboard',
  data () {
    return {
      page: '指标仪表盘',

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

      indicators: [
        [{ label: '城镇人口失业率', value: 'indicator1', type: 'indicator' },
        { label: '+', value: 'add', type: 'operator' },
        { label: '国民生产总值', value: 'indicator2', type: 'indicator' },
        ],
        [{ label: '沪深300（月）', value: 'indicator3', type: 'indicator' },
        { label: '-', value: 'minus', type: 'operator' },
        { label: '黄金现货Au9999（月）', value: 'indicator4', type: 'indicator' },
        { label: '/', value: 'sub', type: 'operator' },
        { label: '黄金现货Au9999（月）', value: 'indicator5', type: 'indicator' },
        { label: '*', value: 'mul', type: 'operator' },
        { label: '100', value: '100', type: 'number' },]
      ],

      dialogVisible: true,
      selectedIndicatorValue: null,
      selectedOperatorValue: null,
      addedNumber: null,
      indicatorMenu: [
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
      ],
      operatorMenu: [
        {
          label: '普通运算符',
          value: 'operatoins',
          children: [
            {
              label: '+',
              value: 'add',
            }, {
              label: '-',
              value: 'minus',
            }, {
              label: '*',
              value: 'mul',
            }, {
              label: '/',
              value: 'div',
            }
          ]
        }
      ],
      filterNodeMethod: (value, data) => data.label.includes(value),

      formular: [
        { label: '沪深300（月）', value: 'indicator3', type: 'indicator' },
        { label: '-', value: 'minus', type: 'operator' },
        { label: '黄金现货Au9999（月）', value: 'indicator4', type: 'indicator' },
        { label: '/', value: 'div', type: 'operator' },
        { label: '黄金现货Au9999（月）', value: 'indicator5', type: 'indicator' },
        { label: '*', value: 'mul', type: 'operator' },
        { label: '100', value: '100', type: 'number' },
      ],
      onTagClose: (index) => {
        this.formular.splice(index, 1);
      },
    }
  },
  components: {
    SideChat,
    VersionFooter,
    Minus,
    Plus
  }
}
</script>