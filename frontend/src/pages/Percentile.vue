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
      <div v-for="m in months" :key="m" :id="`expected-return-${m}-chart`"
        style="width: 100%; height: 270px; margin-top: 20px;"></div>
      <el-divider style="width: 80%; margin-left: 10%; margin-top: 40px"></el-divider>
      <el-row style="margin-top: 40px;">
        <el-col>
          <span style="font-size: var(--el-font-size-large); font-weight: bold;">TL;DR</span>
        </el-col>
      </el-row>
      <el-row style="margin-top: 10px;">
        <el-col>
          <span style="font-size: var(--el-font-size-medium); font-weight: bold">价格偏高</span>
        </el-col>
      </el-row>
      <el-row style="margin-top: 10px;">
        <el-col>
          <el-table :data="TLDRShortData" table-layout="auto">
            <template #empty>
              Loading ...
            </template>
            <el-table-column prop="rank" label="排名"></el-table-column>
            <el-table-column v-for="title in percentileTitles" :key="title" :label="title"
              :prop="title"></el-table-column>
          </el-table>
        </el-col>
      </el-row>
      <el-row style="margin-top: 40px;">
        <el-col>
          <span style="font-size: var(--el-font-size-medium); font-weight: bold; ">价格偏低</span>
        </el-col>
      </el-row>
      <el-row style="margin-top: 10px;">
        <el-col>
          <el-table :data="TLDRLongData" table-layout="auto">
            <template #empty>
              Loading ...
            </template>
            <el-table-column prop="rank" label="排名"></el-table-column>
            <el-table-column v-for="title in percentileTitles" :key="title" :label="title"
              :prop="title"></el-table-column>
          </el-table>
        </el-col>
      </el-row>
      <div id="percentile-chart" style="width: 100%; height: 500px; margin-top: 40px;"></div>
      <side-chat :page="page" />
    </el-main>
    <el-footer>
      <version-footer />
    </el-footer>
  </el-container>
</template>

<script>
import VersionFooter from '../components/VersionFooter.vue';
import SideChat from '../components/SideChat.vue';
import {
  initGraph,
  drawPercentileGraph,
  drawExpectedReturnGraph
} from '../scripts/graph';
import {
  getPricePercentileRequest,
  getExpectedReturnRequest
} from '../scripts/requests';
import { FOLLOWED_DATA, PERCENTILE_PERIOD_WINDOW, PERCENTILE_CHART_TRANSLATION } from '../scripts/constant';

function generateTitle (period, window) {
  return `${PERCENTILE_CHART_TRANSLATION[period]}价格（${window > 0 ? window + '年' : '至今'}）`;
}

export default {
  name: 'Percentile',
  data () {
    return {
      page: '潜在机会',

      percentileTitles: PERCENTILE_PERIOD_WINDOW.map(item => generateTitle(item.period, item.window)),
      percentileData: PERCENTILE_PERIOD_WINDOW.map(item => ({
        period: item.period,
        window: item.window,
        percentile: {}
      })),
      months: [6, 12, 24],
      p: 0.9,
      expectedReturnGraphGroup: {},

      TLDRTopK: 5,
      TLDRLongData: [],
      TLDRShortData: [],

      preparePercentileData: async (pw) => {
        const percentileData = await getPricePercentileRequest({
          'period_window': pw,
          'data': FOLLOWED_DATA.filter(item => !item.skipPercentile)
        });
        for (const item of percentileData.data) {
          const index = this.percentileData.findIndex(p => p.period === item.period && p.window === item.window);
          this.percentileData[index].percentile = item.percentile;
        }
        console.log(this.percentileData);
      },
      prepareTLDRData: () => {
        const dataList = [];
        for (const pData of this.percentileData) {
          const sortedPercentile = Object.entries(pData.percentile)
            .sort(([, a], [, b]) => a - b)
            .map(([k,]) => k);
          dataList.push({
            period: pData.period,
            window: pData.window,
            short: sortedPercentile.slice(-this.TLDRTopK).reverse(),
            long: sortedPercentile.slice(0, this.TLDRTopK)
          });
        }

        this.TLDRShortData = Array.from({ length: this.TLDRTopK }, () => new Object());
        this.TLDRLongData = Array.from({ length: this.TLDRTopK }, () => new Object());

        for (const data of dataList) {
          for (let i = 0; i < this.TLDRTopK; i++) {
            const column = generateTitle(data.period, data.window);
            this.TLDRLongData[i].rank = i + 1;
            this.TLDRShortData[i].rank = i + 1;
            this.TLDRShortData[i][column] = data.short[i];
            this.TLDRLongData[i][column] = data.long[i];
          }
        }
        console.log(this.TLDRShortData);
        console.log(this.TLDRLongData);
      },
      initPercentileGraph: () => {
        this.percentileGraph = initGraph('percentile-chart');
      },
      initExpectedReturnGraph: () => {
        this.months.forEach(m => {
          this.expectedReturnGraphGroup[m] = initGraph(`expected-return-${m}-chart`);
        });
      },
      drawEmptyPercentile: () => {
        drawPercentileGraph(this.percentileGraph, this.percentileData, this.percentileTitles);
        this.percentileGraph.showLoading();
      },
      drawEmptyExpectedReturn: () => {
        this.months.forEach(m => {
          drawExpectedReturnGraph(this.expectedReturnGraphGroup[m], [], m, this.p);
          this.expectedReturnGraphGroup[m].showLoading();
        });
      },
      drawPercentile: async () => {
        for (const periodWindow of PERCENTILE_PERIOD_WINDOW) {
          await this.preparePercentileData([periodWindow]);
          drawPercentileGraph(this.percentileGraph, this.percentileData, this.percentileTitles);
        }
        this.percentileGraph.hideLoading();
      },
      drawExpectedReturn: async () => {
        const draw = async (m) => {
          const expReturnData = await getExpectedReturnRequest({
            'data': FOLLOWED_DATA.filter(item => !item.skipExpReturn),
            'dt': m * 21,
            'p': this.p
          });
          console.log(expReturnData);
          drawExpectedReturnGraph(this.expectedReturnGraphGroup[m], expReturnData.data, m, this.p);
          this.expectedReturnGraphGroup[m].hideLoading();
        };

        const promises = [];
        for (const m of this.months) {
          promises.push(await draw(m));
        }
        await Promise.all(promises);
      }
    }
  },
  async mounted () {
    this.initPercentileGraph();
    this.initExpectedReturnGraph();
    this.drawEmptyPercentile();
    this.drawEmptyExpectedReturn();
    await Promise.all([
      this.drawPercentile(),
      this.drawExpectedReturn()
    ]);
    console.log(this.percentileData);
    this.prepareTLDRData();
  },
  unmounted () {
    this.percentileGraph.dispose();
    for (const m of this.months) {
      this.expectedReturnGraphGroup[m].dispose();
    }
  },
  components: {
    VersionFooter,
    SideChat
  }
}
</script>