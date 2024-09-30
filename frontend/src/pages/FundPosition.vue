<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>基金持仓明细</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
      <el-col :span="6" :offset="9">
        <span style="font-size: var(--el-font-size-large); font-weight: bold">基金持仓明细</span>
      </el-col>
    </el-row>
    <el-row style="width: 70%; margin-left: 15%; margin-bottom: 15px">
      <el-collapse accordion style="width: 100%;">
        <el-collapse-item name="1">
          <template #title>
            <span style="font-size: var(--el-font-size-medium); font-weight: bold">基金名称基金名称基金名称</span>
            <span style="font-size: var(--el-font-size-base); margin-left: 20px">000000</span>
          </template>

          <el-collapse accordion style="width: 95%; margin-left: 5%">
            <el-collapse-item name="11" title="股票">
              <div>
                股票内容
              </div>
            </el-collapse-item>
          </el-collapse>

        </el-collapse-item>
        <el-collapse-item title="Feedback" name="2">
          <div>
            Operation feedback: enable the users to clearly perceive their
            operations by style updates and interactive effects;
          </div>
          <div>
            Visual feedback: reflect current state by updating or rearranging
            elements of the page.
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-row>
  </div>
</template>

<script>

export default {
  name: 'FundPosition',
  data () {
    return {
      activeName: '',
    };
  },
  methods: {
    goBack () {
      this.$router.go(-1);
    },
  },
}
</script>