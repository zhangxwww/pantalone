<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>基金持仓明细</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <el-row justify="center">
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
        <el-col :span="3" :offset="4">
          <el-input v-model="searchFundCode" placeholder="请输入基金代码" @keyup.enter="searchFund" />
        </el-col>
        <el-col :span="1" style="margin-left: 10px;">
          <el-button type="primary" @click="searchFund">
            <el-icon>
              <search />
            </el-icon>
          </el-button>
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
              <span style="font-size: var(--el-font-size-base); margin-left: 20px">
                <el-tag v-if="holding.holdingState" color="#5470c6" size="small" round effect="dark" class="line">
                  {{ '已持有' }}
                </el-tag>
                <el-tag v-else color="#91cc75" size="small" round effect="light" style="color: black" class="line">
                  {{ '未持有' }}
                </el-tag>
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
    </el-main>
  </el-container>
</template>

<script>
import { Search } from '@element-plus/icons-vue';
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
      holdingFunds: [],
      notHoldingFunds: [],

      isReady: false,
      searchFundCode: '',

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

    async searchFund () {
      if (this.searchFundCode === '') {
        return;
      }
      this.drawEmptyRelevanceChart();
      this.notHoldingFunds.push(this.searchFundCode);
      this.searchFundCode = '';
      const [holding, state] = await this.updateHoldings([...this.holdingFunds, ...this.notHoldingFunds]);
      await this.drawRelevanceChart(holding, state);
    },

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
          holdingState: this.holdingFunds.includes(fundCode),
          fundName: await this.getFundName(fundCode),
          stockHoldings: stockHoldings.slice(0, 10),
          bondHoldings: bondHoldings.slice(0, 10)
        };
      });
      const results = await Promise.all(promises);
      this.holdingData.splice(0, this.holdingData.length);
      this.holdingData.push(...results);

      console.log(this.holdingData);
      this.isReady = true;

      const holdingState = {};

      for (const symbol of symbols) {
        holdingState[symbol] = this.holdingFunds.includes(symbol);
      }

      console.log(holding, holdingState);

      return [holding, holdingState];
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

    async drawRelevanceChart (holding, state) {
      const data = await getFundHoldingRelevanceDataRequest(holding);
      console.log(data);
      const relevance = data.relevance;
      const promise = relevance.order.map(async code => await this.getFundName(code));
      relevance.name = await Promise.all(promise);

      drawRelevanceScatterGraph(this.relStockGraph, relevance, state, '股票持仓', 'stockPos');
      drawRelevanceScatterGraph(this.relBondGraph, relevance, state, '债券持仓', 'bondPos');
      drawRelevanceScatterGraph(this.relAllGraph, relevance, state, '全部持仓', 'allPos');
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
    this.holdingFunds.push(...this.$route.query.symbols);
    this.initGraph();
    this.drawEmptyRelevanceChart();
    const [holding, state] = await this.updateHoldings(this.holdingFunds);
    await this.drawRelevanceChart(holding, state);
  },
  unmounted () {
    this.relStockGraph.dispose();
    this.relBondGraph.dispose();
    this.relAllGraph.dispose();
  },
  components: {
    Search
  }
}
</script>