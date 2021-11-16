<template>
  <div>
    <el-row
      align='middle'
    >
      <el-col
        :xl='8'
        :sm='6'
        :span='8'
      >
        <el-button
          size='medium'
          @click='$router.push({name: "admin.workouts"})'
        >
          <el-icon>
            <arrow-left-bold />
          </el-icon>
          Back
        </el-button>
      </el-col>
      <el-col
        :xl='6'
        :sm='12'
        :span='16'
      >
        <h4 style='display: inline-block'>
          {{ workout.title }}
        </h4>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table
          :data='exercises'
        >
          <el-table-column label='Exercise'>
            <template #default='{ row }'>
              {{ row.name }}
            </template>
          </el-table-column>
          <el-table-column label='Info'>
            <template #default='{ row }'>
              {{ row.sets }} sets x {{ row.value }} {{ row.value_type }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import { ArrowLeftBold } from '@element-plus/icons';
  import {
    ElButton,
    ElCol,
    ElIcon,
    ElRow,
    ElTable,
    ElTableColumn,
  } from 'element-plus';

  import { useRoute } from 'vue-router';
  import { exercises } from '../../data/exercise';
  import { workouts } from '../../data/workouts';

  export default {
    components: {
      ElRow,
      ElCol,
      ElTable,
      ElTableColumn,
      ElButton,
      ElIcon,

      ArrowLeftBold,
    },
    setup() {
      const route = useRoute();

      return {
        workout: workouts.find(el => el.id === parseInt(route.params.id)),
        exercises: exercises,
      };
    },
  };
</script>