<template>
  <div>
    <el-row
      justify='space-between'
      align='middle'
    >
      <el-col
        :span='5'
        :xs='{span: 3}'
      >
        <h4>Workouts</h4>
      </el-col>
      <el-col
        :span='10'
        :xs='{span: 15}'
      >
        <el-input
          v-model='search'
          placeholder='Type to search'
          size='mini'
        />
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-scrollbar
          :height='tableHeight'
          :native='false'
        >
          <el-table
            v-loading='loading'
            :data='workouts.filter((data) => !search || data.title.toLowerCase().includes(search.toLowerCase()))'
            :row-class-name='tableRowClassName'
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
                <el-button
                  :loading='row.loading'
                  size='small'
                  @click='$evt => handleWorkoutDone($evt, row, !row.done)'
                >
                  Mark as <span v-if='row.done'>not done</span><span v-else>done</span>
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {
    ElButton,
    ElCol,
    ElInput,
    ElRow,
    ElTable,
    ElTableColumn,
    ElScrollbar,
  } from 'element-plus';

  import {
    computed,
    onMounted,
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
      ElButton,
      ElScrollbar,
    },
    setup() {
      let loading = ref(false);

      const store = useStore();
      const router = useRouter();

      const workouts = computed(() => store.getters['workout/workouts']);
      onMounted(() => {
        loading.value = true;
        store.dispatch(`workout/getAll`).then(_ => {
          loading.value = false;
        });
      });

      const tableRowClassName = ({ row }) => {
        return row.done ? 'primary-row' : '';
      };

      const handleCurrentChange = (workout) => {
        return router.push({
          name: 'admin.workouts.detail',
          params: {
            id: workout.id,
          },
        });
      };

      const handleWorkoutDone = ($evt, workout, done) => {
        $evt.stopPropagation();
        workout.loading = true;
        store.dispatch('workout/setWorkoutDone', { workout: workout.id, done: done })
          .then(_ => {
            workout.done = done;
            workout.loading = false;
          });
      };
      const tableHeight = computed(() => {
        let body = document.body;
        let html = document.documentElement;

        let height = Math.max(
          body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight, html.offsetHeight,
        );

        return `${height - 230}px`;
      });

      return {
        workouts: workouts,
        loading: loading,
        search: ref(''),

        tableRowClassName,
        handleCurrentChange,
        handleWorkoutDone,
        tableHeight,
      };
    },
  };
</script>

<style>
.el-table .primary-row {
  --el-table-tr-background-color: var(--el-color-primary-light-7);
}

.el-table__row {
  cursor: pointer;
  border-radius: 25px;
}

th {
  color: black;
}
</style>