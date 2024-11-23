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
import { initGraph, drawPercentileGraph } from '../scripts/graph';
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
      graph: null,
      percentileData: PERCENTILE_PERIOD_WINDOW.map(item => ({
        period: item.period,
        window: item.window,
        percentile: {}
      })),

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
        this.graph = initGraph('percentile-chart');
      },
      drawEmptyPercentileGraph: () => {
        drawPercentileGraph(this.graph, this.percentileData);
        this.graph.showLoading();
      },
      drawPercentileGraph: async () => {
        drawPercentileGraph(this.graph, this.percentileData);
      },
      draw: async () => {
        const expReturnData = await getExpectedReturnRequest({
          'data': FOLLOWED_DATA.filter(item => !item.skipExpReturn)
        });
        console.log(expReturnData);

        for (const periodWindow of PERCENTILE_PERIOD_WINDOW) {
          await this.prepareData([periodWindow]);
          await this.drawPercentileGraph();
        }
        this.graph.hideLoading();
      }
    }
  },
  async mounted () {
    this.initPercentileGraph();
    this.drawEmptyPercentileGraph();
    await this.draw();
  },
  components: {
    VersionFooter,
    SideChat
  }
}
</script>