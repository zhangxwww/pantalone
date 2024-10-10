<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>基金持仓明细</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row justify="center" style="margin-top: 60px">
      <el-col :span="7">
        <div id="relevance-stock" style="width: 100%; height: 300px"></div>
      </el-col>
      <el-col :span="7">
        <div id="relevance-bond" style="width: 100%; height: 300px"></div>
      </el-col>
      <el-col :span="7">
        <div id="relevance-all" style="width: 100%; height: 300px"></div>
      </el-col>
    </el-row>
    <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
      <el-col :span="6" :offset="9">
        <span style="font-size: var(--el-font-size-large); font-weight: bold">基金持仓明细</span>
      </el-col>
    </el-row>
    <el-row v-if="isReady" style="width: 70%; margin-left: 15%; margin-bottom: 15px">
      <el-collapse accordion style="width: 100%">
        <el-collapse-item v-for="holding in holdingData" :key="holding.fundCode" :name="holding.fundCode">
          <template #title>
            <span style="font-size: var(--el-font-size-medium); font-weight: bold">
              {{ holding.fundName }}
            </span>
            <span style="font-size: var(--el-font-size-base); margin-left: 20px">
              {{ holding.fundCode }}
            </span>
          </template>

          <el-row>
            <el-col :span="12">
              <el-table :data="holding.stockHoldings" table-layout="auto">
                <el-table-column v-for="header in headers.stock" :key="header.prop" :prop="header.prop"
                  :label="header.label" :width="header.width" :align="header.align" show-overflow-tooltip />
              </el-table>
            </el-col>
            <el-col :span="12">
              <el-table :data="holding.bondHoldings" table-layout="auto">
                <el-table-column v-for="header in headers.bond" :key="header.prop" :prop="header.prop"
                  :label="header.label" :width="header.width" :align="header.align" show-overflow-tooltip />
              </el-table>
            </el-col>
          </el-row>
        </el-collapse-item>
      </el-collapse>
    </el-row>
    <el-skeleton v-else :rows="5" animated
      style="width: 70%; margin-left: 15%; margin-bottom: 15px; margin-top: 30px; text-align: left;" />
  </div>
</template>

<script>
import {
  getFundHoldingDataRequest,
  getFundNameRequest,
  getFundHoldingRelevanceDataRequest
} from '../scripts/requests';
import {
  initGraph,
  drawRelevanceScatterGraph,
  drawEmptyRelevanceScatterGraph
} from '../scripts/graph';

export default {
  name: 'FundPosition',
  data () {
    return {
      holdingData: [],

      isReady: false,

      headers: {
        stock: [
          { prop: 'name', label: '股票名称', width: '150', align: 'left' },
          { prop: 'code', label: '股票代码', width: '100', align: 'right' },
          { prop: 'ratio', label: '占净值比例', width: '100', align: 'right' },
          { prop: 'updatedAt', label: '更新时间', width: '100', align: 'right' }
        ],
        bond: [
          { prop: 'name', label: '债券名称', width: '150', align: 'left' },
          { prop: 'code', label: '债券代码', width: '100', align: 'right' },
          { prop: 'ratio', label: '占净值比例', width: '100', align: 'right' },
          { prop: 'updatedAt', label: '更新时间', width: '100', align: 'right' }
        ]
      }
    };
  },
  methods: {

    async updateHoldings (symbols) {
      this.isReady = false;

      const data = await getFundHoldingDataRequest(symbols);
      const holding = data.holding;

      console.log(holding);

      const promises = Object.entries(holding).map(async ([fundCode, holdings]) => {
        const stockHoldings = holdings
          .stock
          .sort((a, b) => b.ratio - a.ratio)
          .map(holding => {
            return {
              name: holding.name,
              code: holding.code,
              ratio: `${holding.ratio.toFixed(2)}%`,
              updatedAt: `${holding.year}-Q${holding.quarter}`
            };
          });
        const bondHoldings = holdings
          .bond
          .sort((a, b) => b.ratio - a.ratio)
          .map(holding => {
            return {
              name: holding.name,
              code: holding.code,
              ratio: holding.ratio,
              updatedAt: `${holding.year}-Q${holding.quarter}`
            };
          });
        return {
          fundCode: fundCode,
          fundName: await this.getFundName(fundCode),
          stockHoldings: stockHoldings.slice(0, 10),
          bondHoldings: bondHoldings.slice(0, 10)
        };
      });
      const results = await Promise.all(promises);
      this.holdingData.push(...results);

      console.log(this.holdingData);
      this.isReady = true;

      return holding;
    },

    async getFundName (symbol) {
      const data = await getFundNameRequest(symbol);
      return data.fund_name;
    },

    initGraph () {
      this.relStockGraph = initGraph('relevance-stock');
      this.relBondGraph = initGraph('relevance-bond');
      this.relAllGraph = initGraph('relevance-all');
    },

    setAllGraphLoading () {
      this.relAllGraph.showLoading();
      this.relStockGraph.showLoading();
      this.relBondGraph.showLoading();
    },

    setAllGraphUnloading () {
      this.relAllGraph.hideLoading();
      this.relStockGraph.hideLoading();
      this.relBondGraph.hideLoading();
    },

    async drawRelevanceChart (holding) {
      const data = await getFundHoldingRelevanceDataRequest(holding);
      console.log(data);
      const relevance = data.relevance;
      const promise = relevance.order.map(async code => await this.getFundName(code));
      relevance.name = await Promise.all(promise);

      drawRelevanceScatterGraph(this.relStockGraph, relevance, '股票持仓', 'stockPos');
      drawRelevanceScatterGraph(this.relBondGraph, relevance, '债券持仓', 'bondPos');
      drawRelevanceScatterGraph(this.relAllGraph, relevance, '全部持仓', 'allPos');
      this.setAllGraphUnloading();
    },

    drawEmptyRelevanceChart () {
      drawEmptyRelevanceScatterGraph(this.relStockGraph, '股票持仓', 'stockPos');
      drawEmptyRelevanceScatterGraph(this.relBondGraph, '债券持仓', 'bondPos');
      drawEmptyRelevanceScatterGraph(this.relAllGraph, '全部持仓', 'allPos');
      this.setAllGraphLoading();
    },


  },
  async mounted () {
    console.log(this.$route.query.symbols);
    this.initGraph();
    this.drawEmptyRelevanceChart();
    const holding = await this.updateHoldings(this.$route.query.symbols);
    await this.drawRelevanceChart(holding);
  },
  unmounted () {
    this.relStockGraph.dispose();
    this.relBondGraph.dispose();
    this.relAllGraph.dispose();
  }
}
</script>