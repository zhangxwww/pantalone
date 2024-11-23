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
import { FOLLOWED_DATA, PERCENTILE_PERIOD_WINDOW } from '../scripts/constant';

export default {
  name: 'Percentile',
  data () {
    return {
      page: '潜在机会',
      percentileData: PERCENTILE_PERIOD_WINDOW.map(item => ({
        period: item.period,
        window: item.window,
        percentile: {}
      })),
      months: [6, 12, 24],
      p: 0.95,
      expectedReturnGraphGroup: {},

      prepareData: async (pw) => {
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
      initPercentileGraph: () => {
        this.percentileGraph = initGraph('percentile-chart');
      },
      initExpectedReturnGraph: () => {
        this.months.forEach(m => {
          this.expectedReturnGraphGroup[m] = initGraph(`expected-return-${m}-chart`);
        });
      },
      drawEmptyPercentile: () => {
        drawPercentileGraph(this.percentileGraph, this.percentileData);
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
          await this.prepareData([periodWindow]);
          drawPercentileGraph(this.percentileGraph, this.percentileData);
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
  },
  unmounted () {
    this.percentileGraph.dispose();
    this.expectedReturnGraph.dispose();
  },
  components: {
    VersionFooter,
    SideChat
  }
}
</script>