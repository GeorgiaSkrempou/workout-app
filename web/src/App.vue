<template>
  <el-container>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
  import {
    ElContainer,
    ElMain,
  } from 'element-plus';

  export default {
    components: {
      ElContainer,
      ElMain,
    },
  };
</script>
