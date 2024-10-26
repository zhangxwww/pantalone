<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>百分位分析</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
        <el-col :span="6" :offset="9">
          <span style="font-size: var(--el-font-size-large); font-weight: bold">百分位分析</span>
        </el-col>
      </el-row>
      <div id="percentile-chart" style="width: 100%; height: 500px"></div>
    </el-main>
    <el-footer>
      <version-footer />
    </el-footer>
  </el-container>
</template>

<script>
import VersionFooter from '../components/VersionFooter.vue';
import { initGraph, drawPercentileGraph } from '../scripts/graph';
import { getPricePercentileRequest } from '../scripts/requests';
import { FOLLOWED_DATA, PERCENTILE_PERIOD_WINDOW } from '../scripts/constant';

export default {
  name: 'Percentile',
  data () {
    return {
      graph: null,
      percentileData: [],

      prepareEmptyData: () => {
        return PERCENTILE_PERIOD_WINDOW.map(item => ({
          period: item.period,
          window: item.window,
          percentile: {}
        }));
      },
      prepareData: async () => {
        const data = await getPricePercentileRequest({
          'period_window': PERCENTILE_PERIOD_WINDOW,
          'data': FOLLOWED_DATA.filter(item => !item.skipPercentile)
        });
        this.percentileData = data.data;
        console.log(this.percentileData);
      },
      initPercentileGraph: () => {
        this.graph = initGraph('percentile-chart');
      },
      drawEmptyPercentileGraph: () => {
        drawPercentileGraph(this.graph, this.prepareEmptyData());
        this.graph.showLoading();
      },
      drawPercentileGraph: async () => {
        drawPercentileGraph(this.graph, this.percentileData);
        this.graph.hideLoading();
      }
    }
  },
  async mounted () {
    this.initPercentileGraph();
    this.drawEmptyPercentileGraph();
    await this.prepareData();
    await this.drawPercentileGraph();
  },
  components: {
    VersionFooter
  }
}
</script>