<template>
  <span style="font-size: var(--el-font-size-extra-small);">
    Backend: v{{ backendVersion }} | Frontend: v{{ frontendVersion }}
  </span>
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