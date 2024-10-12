<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>行情看板</el-breadcrumb-item>
    </el-breadcrumb>
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
    <div v-for="(c, i) in groupedConfig" :key="i">
      <el-divider style="margin-top: 60px; margin-left: 10%; width: 80%;">
        <b>{{ c.category }}</b>
      </el-divider>
      <el-row v-for="content in c.grouped" :key="content" justify="left">
        <el-col v-for="item in content" :key="item" :span="8">
          <div :id="`${item.name}${item.code}`" style="width: 100%; height: 300px">
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
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
      config: [
        {
          category: '指数',
          content: [
            {
              name: '上证综指',
              code: '000001',
              market: 'index-CN'
            },
            {
              name: '国债指数',
              code: '000012',
              market: 'index-CN'
            },
            {
              name: '上证综指2',
              code: '000001',
              market: 'index-CN'
            },
          ]
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
              drawKLineGraph(graph, [], title);
              graph.showLoading();

              const res = await getKLineDataRequest(item.code, this.period, item.market);
              console.log(res);

              drawKLineGraph(graph, res.kline, title);
              graph.hideLoading();
            }
            promises.push(promise(item));
          }
        }
        await Promise.all(promises);
      },
    };
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