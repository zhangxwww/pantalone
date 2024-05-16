<template>
  <el-row>
    <el-col :span="15">
      <div id="main"
           style="width: 900px; height: 300px"></div>
    </el-col>
    <el-col :span="9">
      <el-row>
        <el-dropdown trigger="hover"
                     v-on:command="onAddSelect">
          <el-button type="primary"
                     @click="onAddClick">
            <el-icon>
              <plus />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="1">1</el-dropdown-item>
              <el-dropdown-item command="2">2</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button>
          <el-icon>
            <download />
          </el-icon>
        </el-button>
        <el-button>
          <el-icon>
            <upload />
          </el-icon>
        </el-button>
      </el-row>
      <el-tabs type="border-card"
               :v-model="table_tab_name">
        <el-tab-pane label="User">
          <el-table :data="tableData"
                    height="500"
                    style="width: 100%">
            <el-table-column prop="date"
                             label="Date"
                             width="180"
                             :sortable="true" />
            <el-table-column prop="name"
                             label="Name"
                             width="180" />
            <el-table-column prop="address"
                             label="Address" />
            <el-table-column label="Operations">
              <template #default="scope">
                <el-button size="small"
                           @click="handleEdit(scope.$index, scope.row)">
                  Edit
                </el-button>
                <el-button size="small"
                           type="danger"
                           @click="handleDelete(scope.$index, scope.row)">
                  Delete
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="Config">Config</el-tab-pane>
        <el-tab-pane label="Role">Role</el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
import * as echarts from "echarts"
import {
  Plus,
  Download,
  Upload
} from '@element-plus/icons-vue'


export default {
  name: 'MainPage',
  data () {
    return {
      chart: null,
      table_tab_name: String,

      tableData: [
        {
          date: '2016-05-03',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 0
        },
        {
          date: '2016-05-02',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 1
        },
        {
          date: '2016-05-04',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 2
        },
        {
          date: '2016-05-01',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 3
        },
        {
          date: '2016-05-08',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 4
        },
        {
          date: '2016-05-06',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 5
        },
        {
          date: '2016-05-07',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles',
          id: 6
        },
      ],
      handleEdit: (index, row) => {
        console.log(row.id)
      },
      handleDelete: (index, row) => {
        console.log(index, row)
      },
      onAddClick: () => {
        console.log('click add')
      },
      onAddSelect: type => {
        console.log(type)
      }
    }
  },
  components: {
    Plus,
    Download,
    Upload
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
  },

}
</script>