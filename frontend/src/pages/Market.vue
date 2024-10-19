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
          <el-radio-group v-model="period" @change="updateGraph(true)" size="small">
            <el-radio-button label="日K" value="daily" />
            <el-radio-button label="周K" value="weekly" />
            <el-radio-button label="月K" value="monthly" />
          </el-radio-group>
        </el-col>
        <el-col :span="5">
          <el-select v-model="indicator.value" @change="onIndicatorChange" placeholder="选择技术指标" size="small"
            style="width: 45%">
            <el-option label="NONE" value="" />
            <el-option label="BOLL" value="boll" />
          </el-select>
        </el-col>
      </el-row>

      <el-tabs v-model="category" @tab-change="onTabChange">
        <el-tab-pane v-for="(c, i) in groupedConfig" :key="i" :label="c.category" :name="c.category">
          <el-row v-for="content in c.grouped" :key="content" justify="left" style="margin-bottom: 20px;">
            <el-col v-for="item in content" :key="item" :span="8">
              <div :id="`${item.name}${item.code}`" style="width: 100%; height: 500px">
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
  drawKLineGraph,
  drawMarketPriceLineGraph,
  drawEmptyMarketPriceLineGraph
} from '../scripts/graph';
import {
  getKLineDataRequest,
  getMarketDataRequest
} from '../scripts/requests'

export default {
  data () {
    return {
      period: 'daily',
      indicator: {
        value: '',
        config: {
          boll: {
            window: 20,
            width: 2
          }
        }
      },
      category: '',
      config: [
        {
          category: 'A股指数',
          isKLine: true,
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
          category: '美股指数',
          isKLine: true,
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
            }
          ]
        },
        {
          category: '港股指数',
          isKLine: true,
          content: [
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
          category: '波动率指数',
          isKLine: true,
          content: [
            {
              name: '50ETF期权波动率指数QVIX',
              code: '50ETF',
              market: 'index-qvix'
            },
            {
              name: '300ETF期权波动率指数QVIX',
              code: '300ETF',
              market: 'index-qvix'
            }
          ]
        },
        {
          category: '债券指数',
          isKLine: true,
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
          isKLine: true,
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
          isKLine: true,
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
          isKLine: true,
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
          isKLine: false,
          content: [
            {
              name: 'LPR品种',
              code: '',
              instrument: 'LPR'
            }
          ]
        },
        {
          category: '外汇',
          isKLine: false,
          content: []
        },
        {
          category: '宏观',
          isKLine: false,
          content: []
        },
        {
          category: '全球宏观',
          isKLine: false,
          content: []
        }
      ],
      cache: {},

      initGraph: () => {
        this.graphs = {};
        for (const cat of this.config) {
          for (const item of cat.content) {
            const dom = `${item.name}${item.code}`;
            this.graphs[item.name] = initGraph(dom);
          }
        }
      },

      getGraph: (name) => {
        return this.graphs[name];
      },

      getGraphTitle: (name, code) => {
        return code ? `${name}（${code}）` : name;
      },

      drawEmptyGraph: (name, title, isKLine) => {
        const graph = this.getGraph(name);
        if (isKLine) {
          drawKLineGraph(graph, [], title, this.period, this.indicator);
        } else {
          drawEmptyMarketPriceLineGraph(graph, title);
        }
        graph.showLoading();
        return graph;
      },

      getCacheKey: (title, isKLine) => {
        return isKLine ? `${this.period}-${title}` : title;
      },

      getKLineData: async (key, code, market) => {
        let kline;
        if (key in this.cache) {
          kline = this.cache[key];
        } else {
          const res = await getKLineDataRequest(code, this.period, market);
          console.log(res);
          kline = res.kline;
          for (let i = 0; i < this.indicator.config.boll.window; i++) {
            kline[i].mid = Number.NaN;
            kline[i].lower = Number.NaN;
            kline[i].upper = Number.NaN;
          }
          this.cache[key] = kline;
        }
        return kline;
      },

      getMarketPriceData: async (key, instrument) => {
        let data;
        if (key in this.cache) {
          data = this.cache[key];
        } else {
          const res = await getMarketDataRequest(instrument);
          data = res.market;
          this.cache[key] = data;
        }
        return data;
      },

      drawKLineGraph: (graph, kline, title) => {
        drawKLineGraph(graph, kline, title, this.period, this.indicator);
        graph.hideLoading();
      },

      drawMarketPriceLineGraph: (graph, data, title) => {
        drawMarketPriceLineGraph(graph, data, title);
        graph.hideLoading();
      },

      drawOneChart: async (cat, item, clear) => {
        const title = this.getGraphTitle(item.name, item.code);
        const graph = this.drawEmptyGraph(item.name, title, cat.isKLine);
        const key = this.getCacheKey(title, cat.isKLine);
        const data = cat.isKLine
          ? await this.getKLineData(key, item.code, item.market)
          : await this.getMarketPriceData(key, item.instrument);

        if (clear) {
          graph.clear();
        }
        if (cat.isKLine) {
          this.drawKLineGraph(graph, data, title);
        } else {
          this.drawMarketPriceLineGraph(graph, data, title);
        }
      },

      updateGraph: async (skipNotKLine) => {
        const promises = [];
        for (const cat of this.config) {
          if (skipNotKLine && !cat.isKLine) {
            continue;
          }
          for (const item of cat.content) {
            const promise = async (item) => {
              await this.drawOneChart(cat, item, false);
            };
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
      },

      onIndicatorChange: async () => {
        localStorage.setItem('market-indicator', this.indicator.value);
        for (const cat of this.config) {
          if (!cat.isKLine) {
            continue;
          }
          for (const item of cat.content) {
            await this.drawOneChart(cat, item, true);
          }
        }
      }

    };
  },
  beforeMount () {
    this.category = localStorage.getItem('market-category') || 'A股指数';
    this.indicator.value = localStorage.getItem('market-indicator') || 'boll';
  },
  async mounted () {
    this.initGraph();
    await this.updateGraph(false);
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