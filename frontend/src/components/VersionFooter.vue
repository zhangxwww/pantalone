<template>
  <div style="margin-bottom: 30px;">
    <el-divider style="width: 20%; margin-left: 40%; margin-bottom: 10px;" />
    <span style="font-size: var(--el-font-size-extra-small);">
      Backend: v{{ backendVersion }} | Frontend: v{{ frontendVersion }}
    </span>
  </div>
</template>

<script>
import { getBackendVersionRequest } from '../scripts/requests';

export default {
  name: 'VersionFooter',
  data () {
    return {
      backendVersion: '',
      frontendVersion: process.env.PACKAGE_VERSION,
    };
  },
  async created () {
    const data = await getBackendVersionRequest();
    this.backendVersion = data.version;
  },
};
</script>