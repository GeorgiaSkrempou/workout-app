<template>
  <div>
    <el-row>
      <el-col>
        <h4>Workouts</h4>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table
          v-if='loading === false'
          :data='workouts.filter((data) => !search || data.title.toLowerCase().includes(search.toLowerCase()))'
          :row-class-name='tableRowClassName'
          :stripe='true'
          max-height='400px'
          @current-change='handleCurrentChange'
        >
          <el-table-column
            label='Day'
            prop='title'
          />
          <el-table-column
            label='Done'
          >
            <template #default='{ row }'>
              <el-icon
                v-if='row.done'
              >
                <circle-check-filled />
              </el-icon>
              <el-icon
                v-else
              >
                <circle-close-filled />
              </el-icon>
            </template>
          </el-table-column>
          <el-table-column align='right'>
            <template #header>
              <el-input
                v-model='search'
                placeholder='Type to search'
                size='mini'
              />
            </template>
          </el-table-column>
        </el-table>
        <el-skeleton
          v-else
          :rows='5'
          animated
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {
    CircleCheckFilled,
    CircleCloseFilled,
  } from '@element-plus/icons';
  import {
    ElCol,
    ElIcon,
    ElInput,
    ElRow,
    ElSkeleton,
    ElTable,
    ElTableColumn,
  } from 'element-plus';

  import {
    computed,
    ref,
  } from 'vue';
  import { useRouter } from 'vue-router';
  import { useStore } from 'vuex';

  export default {
    name: 'Dashboard',
    components: {
      ElRow,
      ElTable,
      ElTableColumn,
      ElInput,
      ElCol,
      ElIcon,
      ElSkeleton,

      CircleCheckFilled,
      CircleCloseFilled,
    },
    setup() {
      let loading = ref(false);

      const store = useStore();
      const router = useRouter();

      const workouts = computed(() => store.getters['workout/workouts']);
      // let loaded = computed(() => store.getters[`workout/workoutsLoaded`]);
      // if (loaded.value === false) {
      loading.value = true;
      store.dispatch(`workout/getAll`).then(_ => {
        loading.value = false;
      });
      // }

      const tableRowClassName = ({ row }) => {
        return row.done ? 'success-row' : '';
      };

      const handleCurrentChange = (workout) => {
        return router.push({
          name: 'admin.workouts.detail',
          params: {
            id: workout.id,
          },
        });
      };

      return {
        workouts: workouts,
        loading: loading,
        search: ref(''),

        tableRowClassName,
        handleCurrentChange,
      };
    },
  };
</script>

<style>
.el-table .success-row {
  --el-table-tr-background-color: var(--el-color-success-lighter);
}
</style>