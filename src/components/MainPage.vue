<template>
  <el-row>
    <el-col :span="18">
      <div id="main"
           style="width: 900px; height: 300px"></div>
    </el-col>
    <el-col :span="6">
    </el-col>
  </el-row>
</template>

<script>
import * as echarts from "echarts"

export default {
  name: 'MainPage',
  data () {
    return {
      chart: null
    }
  },
  mounted () {
    this.chart = echarts.init(document.getElementById('main'))
    this.chart.setOption({
      title: {
        text: 'ECharts 入门示例'
      },
      tooltip: {},
      xAxis: {
        data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
      },
      yAxis: {},
      series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }]
    })
  },
  unmounted () {
    this.chart.dispose()
  }
}
</script>