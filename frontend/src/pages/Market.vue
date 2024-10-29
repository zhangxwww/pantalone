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
      <side-chat :page="page" />
    </el-main>
    <el-footer>
      <VersionFooter />
    </el-footer>
  </el-container>
</template>

<script>
import VersionFooter from '../components/VersionFooter.vue';
import SideChat from '../components/SideChat.vue';
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
import { FOLLOWED_DATA } from '../scripts/constant';

export default {
  data () {
    return {
      page: '行情看板',
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
      config: FOLLOWED_DATA,
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
  components: {
    VersionFooter,
    SideChat
  }
};

</script>