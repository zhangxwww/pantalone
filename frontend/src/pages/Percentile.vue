<template>
  <el-container>
    <el-main>
      <div>
        Percentile
      </div>
    </el-main>
    <el-footer>
      <version-footer />
    </el-footer>
  </el-container>
</template>

<script>
import VersionFooter from '../components/VersionFooter.vue';
export default {
  name: 'Percentile',
  data () {
    return {

    }
  },
  components: {
    VersionFooter
  }
}
</script>