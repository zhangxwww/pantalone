<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>行情看板</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>

    <el-main>
      <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
        <el-col :span="6" :offset="9">
          <span style="font-size: var(--el-font-size-large); font-weight: bold">行情看板</span>
        </el-col>
      </el-row>
      <el-row justify="center">
        <el-col :span="5">
          <el-radio-group v-model="period" @change="updateGraph" size="small">
            <el-radio-button label="日K" value="daily" />
            <el-radio-button label="周K" value="weekly" />
            <el-radio-button label="月K" value="monthly" />
          </el-radio-group>
        </el-col>
        <el-col :span="5">
          <el-select v-model="indicator" placeholder="选择技术指标" size="small" style="width: 45%">
            <el-option label="NONE" value="" />
            <el-option label="BOLL" value="boll" />
          </el-select>
        </el-col>
      </el-row>

      <el-tabs v-model="category" @tab-change="onTabChange">
        <el-tab-pane v-for="(c, i) in groupedConfig" :key="i" :label="c.category" :name="c.category">
          <el-row v-for="content in c.grouped" :key="content" justify="left" style="margin-bottom: 20px;">
            <el-col v-for="item in content" :key="item" :span="8">
              <div :id="`${item.name}${item.code}`" style="width: 100%; height: 300px">
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<script>
import {
  initGraph,
  drawKLineGraph
} from '../scripts/graph';
import {
  getKLineDataRequest
} from '../scripts/requests'

export default {
  data () {
    return {
      period: 'daily',
      indicator: '',
      category: 'A股指数',
      config: [
        {
          category: 'A股指数',
          content: [
            {
              name: '上证综指',
              code: '000001',
              market: 'index-CN'
            },
            {
              name: '深证成指',
              code: '399001',
              market: 'index-CN'
            },
            {
              name: '创业板指',
              code: '399006',
              market: 'index-CN'
            },
            {
              name: '沪深300',
              code: '000300',
              market: 'index-CN'
            },
            {
              name: '北证50',
              code: '899050',
              market: 'index-CN'
            },
            {
              name: '科创50',
              code: '000688',
              market: 'index-CN'
            },
            {
              name: '中证A500',
              code: '000510',
              market: 'index-CN'
            },
            {
              name: '中证1000',
              code: '000852',
              market: 'index-CN'
            },
            {
              name: '中证2000',
              code: '932000',
              market: 'index-CN'
            }
          ]
        },
        {
          category: '全球指数',
          content: [
            {
              name: '纳斯达克综合指数',
              code: '.IXIC',
              market: 'index-US'
            },
            {
              name: '道琼斯工业指数',
              code: '.DJI',
              market: 'index-US'
            },
            {
              name: '标普500指数',
              code: '.INX',
              market: 'index-US'
            },
            {
              name: '纳斯达克100指数',
              code: '.NDX',
              market: 'index-US'
            },
            {
              name: '50ETF期权波动率指数QVIX',
              code: '50ETF',
              market: 'index-qvix'
            },
            {
              name: '300ETF期权波动率指数QVIX',
              code: '300ETF',
              market: 'index-qvix'
            },
            {
              name: '恒生指数',
              code: 'HSI',
              market: 'index-HK'
            },
            {
              name: '恒生科技指数',
              code: 'HSTECH',
              market: 'index-HK'
            },
            {
              name: '恒生中国内地银行指数',
              code: 'HSMBI',
              market: 'index-HK'
            },
            {
              name: '恒生中国内地石油及天然气指数',
              code: 'HSMOGI',
              market: 'index-HK'
            },
            {
              name: '恒生中国内地地产指数',
              code: 'HSMPI',
              market: 'index-HK'
            }
          ]
        },
        {
          category: '板块',
          content: []
        },
        {
          category: '债券',
          content: [
            {
              name: '国债指数',
              code: '000012',
              market: 'index-CN'
            },
            {
              name: '企债指数',
              code: '000013',
              market: 'index-CN'
            },
            {
              name: '公司债指',
              code: '000923',
              market: 'index-CN'
            }
          ]
        },
        {
          category: '商品期货',
          content: [
            {
              name: '黄金连续',
              code: 'AU0',
              market: 'future-zh'
            },
            {
              name: '白银连续',
              code: 'AG0',
              market: 'future-zh'
            },
            {
              name: '铜连续',
              code: 'CU0',
              market: 'future-zh'
            },
            {
              name: '上海原油连续',
              code: 'SC0',
              market: 'future-zh'
            },
          ]
        },
        {
          category: '股指期货',
          content: [
            {
              name: '沪深300指数期货',
              code: 'IF0',
              market: 'future-zh'
            },
            {
              name: '上证50指数期货',
              code: 'IH0',
              market: 'future-zh'
            },
            {
              name: '中证500指数期货',
              code: 'IC0',
              market: 'future-zh'
            }
          ]
        },
        {
          category: '国债期货',
          content: [
            {
              name: '5年期国债期货',
              code: 'TF0',
              market: 'future-zh'
            },
            {
              name: '2年期国债期货',
              code: 'TS0',
              market: 'future-zh'
            }
          ]
        },
        {
          category: '利率',
          content: []
        },
        {
          category: '外汇',
          content: []
        },
        {
          category: '宏观',
          content: []
        },
        {
          category: '全球宏观',
          content: []
        }
      ],

      initGraph: () => {
        this.graphs = {};
        for (const cat of this.config) {
          for (const item of cat.content) {
            const dom = `${item.name}${item.code}`;
            this.graphs[item.name] = initGraph(dom);
          }
        }
      },

      updateGraph: async () => {
        const promises = [];
        for (const cat of this.config) {
          for (const item of cat.content) {
            const promise = async (item) => {
              const graph = this.graphs[item.name];
              const title = `${item.name}（${item.code}）`;
              drawKLineGraph(graph, [], title, this.period);
              graph.showLoading();

              const res = await getKLineDataRequest(item.code, this.period, item.market);
              console.log(res);

              drawKLineGraph(graph, res.kline, title, this.period);
              graph.hideLoading();
            }
            promises.push(promise(item));
          }
        }
        await Promise.all(promises);
      },

      onTabChange: () => {
        for (const chart of Object.values(this.graphs)) {
          this.$nextTick(() => {
            chart.resize();
          })
        }
        localStorage.setItem('market-category', this.category);
      }

    };
  },
  beforeMount () {
    const category = localStorage.getItem('market-category') || 'A股指数';
    this.category = category;
  },
  async mounted () {
    this.initGraph();
    await this.updateGraph();
  },
  computed: {
    groupedConfig () {
      const con = [];
      for (let c of this.config) {
        const groups = [];
        for (let i = 0; i < c.content.length; i += 3) {
          groups.push(c.content.slice(i, i + 3));
        }
        con.push({
          'category': c.category,
          'grouped': groups
        })
      }
      return con;
    },
  },
};

</script>