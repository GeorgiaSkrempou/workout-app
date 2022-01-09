<template>
  <el-container>
    <el-header style='text-align: center; height: auto'>
      <h1>Georgia's and Alex's workout routine</h1>
      <p>No pain no gain </p>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
  import {
    ElContainer,
    ElMain,
    ElHeader,
  } from 'element-plus';

  export default {
    components: {
      ElContainer,
      ElMain,
      ElHeader,
    },
  };
</script>
