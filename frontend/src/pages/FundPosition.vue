<template>
  <el-container>
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ page }}</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <el-row justify="center">
        <el-col :span="20">
          <div id="relation-graph" style="width: 100%; height: 800px"></div>
        </el-col>
      </el-row>
      <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
        <el-col :span="6" :offset="9">
          <span style="font-size: var(--el-font-size-large); font-weight: bold">{{ page }}</span>
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
      <side-chat :page="page" />
    </el-main>
    <el-footer>
      <version-footer />
    </el-footer>
  </el-container>
</template>

<script>
import { Search } from '@element-plus/icons-vue';
import VersionFooter from '../components/VersionFooter.vue';
import SideChat from '../components/SideChat.vue';
import {
  getFundHoldingDataRequest,
  getFundNameRequest,
  getStockBondInfoRequest
} from '../scripts/requests';
import {
  initGraph,
  drawRelationGraph,
} from '../scripts/graph';
import { RelationGraphBuilder } from '../scripts/graphBuilder';

export default {
  name: 'FundPosition',
  data () {
    return {
      page: '基金持仓明细',
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
      this.notHoldingFunds.push(this.searchFundCode);
      this.searchFundCode = '';
      this.relationGraph.showLoading();
      // eslint-disable-next-line no-unused-vars
      const [holding, state] = await this.updateHoldings([...this.holdingFunds, ...this.notHoldingFunds]);
      await this.drawRelationGraph(holding);
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
      this.relationGraph = initGraph('relation-graph')
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


    async drawRelationGraph (holding) {
      let stocks = [];
      let bonds = [];

      const fundHolding = [];
      for (const [fund, h] of Object.entries(holding)) {
        stocks.push(...h.stock.map(hh => hh.code));
        bonds.push(...h.bond.map(hh => hh.code));
        fundHolding.push({
          'fundCode': fund,
          'stocks': h.stock.map(hh => hh.code),
          'bonds': h.bond.map(hh => hh.code)
        });
      }
      stocks = [...new Set(stocks)];
      bonds = [...new Set(bonds)];

      console.log(stocks);
      console.log(bonds);
      console.log(fundHolding);

      const resp = await getStockBondInfoRequest(stocks, bonds);
      const stockBondInfo = resp.data;
      console.log(stockBondInfo);

      const fundName = {};
      for (const f of this.holdingData) {
        fundName[f.fundCode] = f.fundName;
      }
      console.log(fundName);

      const graph = new RelationGraphBuilder(fundName, holding, stockBondInfo).build();
      console.log(graph);

      drawRelationGraph(this.relationGraph, graph);
      this.relationGraph.hideLoading();
    }

  },
  async mounted () {
    console.log(this.$route.query.symbols);
    this.holdingFunds.push(...this.$route.query.symbols);
    this.initGraph();
    this.relationGraph.showLoading();
    // eslint-disable-next-line no-unused-vars
    const [holding, state] = await this.updateHoldings(this.holdingFunds);
    await this.drawRelationGraph(holding);
  },
  unmounted () {
    this.relationGraph.dispose();
  },
  components: {
    Search,
    VersionFooter,
    SideChat
  }
}
</script>