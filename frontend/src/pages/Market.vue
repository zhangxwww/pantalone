<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>全球市场行情</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row justify="center" style="margin-top: 60px">
      <el-col :span="8">
        <div id="test-kline" style="width: 100%; height: 300px"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {
  initGraph,
  drawKLineGraph
} from '../scripts/graph';

export default {
  data () {
    return {
      initGraph () {
        this.klineGraph = initGraph('test-kline');
      },
    };
  },
  mounted () {
    this.initGraph();
    drawKLineGraph(this.klineGraph);
  },
};

</script>