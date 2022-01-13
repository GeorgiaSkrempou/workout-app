<template>
  <div>
    <el-row
      align='middle'
    >
      <el-col
        :sm='6'
        :span='8'
        :xl='8'
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
        :sm='12'
        :span='16'
        :xl='6'
      >
        <h4 style='display: inline-block'>
          {{ workout.title }}
        </h4>
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
            :data='workout.exercises'
          >
            <el-table-column
              v-if='isMobile'
              type='expand'
            >
              <template #default='{ row }'>
                <el-descriptions
                  class='p-3'
                  title='Exercise info'
                  :column='1'
                  border
                >
                  <el-descriptions-item>
                    <template #label>
                      Reps
                    </template>
                    {{ row.value }} {{ row.value_type }}
                  </el-descriptions-item>
                  <el-descriptions-item>
                    <template #label>
                      Sets
                    </template>
                    {{ row.sets }}
                  </el-descriptions-item>
                  <el-descriptions-item>
                    <template #label>
                      Weight
                    </template>
                    {{ row.weight }}
                  </el-descriptions-item>
                </el-descriptions>
              </template>
            </el-table-column>
            <el-table-column
              label='Exercise'
            >
              <template #default='{ row }'>
                {{ row.name }}
              </template>
            </el-table-column>
            <el-table-column
              v-if='isMobile === false'
              label='Info'
            >
              <template #default='{ row }'>
                {{ row.sets }} sets x {{ row.value }} {{ row.value_type }}
              </template>
            </el-table-column>
            <el-table-column
              v-if='isMobile === false'
              label='Weight'
              min-width='100'
              prop='weight'
              width='100'
            />
            <el-table-column
              align='right'
            >
              <template #default='{ row }'>
                <el-button
                  size='small'
                  @click='showWeightModal(row)'
                >
                  Update weight
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
      </el-col>
    </el-row>

    <el-dialog
      v-model='weightModalVisible'
      :title='`Update weight for ${selectedExercise.name}`'
      destroy-on-close
    >
      <el-form>
        <el-form-item
          :label-width='formLabelWidth'
          label='Weight'>
          <el-input
            v-model='weight'
            autocomplete='off'
            autofocus
            type='number'
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class='dialog-footer'>
          <el-button
            @click='weightModalVisible = false'
          >
            Cancel
          </el-button>
          <el-button
            v-loading='savingWeight'
            type='primary'
            @click='saveWeight(selectedExercise)'
          >
            Save
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
  import { ArrowLeftBold } from '@element-plus/icons';
  import {
    ElButton,
    ElCol,
    ElDialog,
    ElForm,
    ElFormItem,
    ElIcon,
    ElInput,
    ElRow,
    ElScrollbar,
    ElTable,
    ElTableColumn,
    ElDescriptions,
    ElDescriptionsItem,
  } from 'element-plus';

  import {
    computed,
    onMounted,
    ref,
  } from 'vue';
  import { useRoute } from 'vue-router';
  import { useStore } from 'vuex';

  export default {
    components: {
      ElRow,
      ElCol,
      ElTable,
      ElTableColumn,
      ElButton,
      ElIcon,
      ElDialog,
      ElForm,
      ElFormItem,
      ElInput,
      ElScrollbar,
      ElDescriptions,
      ElDescriptionsItem,

      ArrowLeftBold,
    },
    setup() {
      let weightModalVisible = ref(false);
      let savingWeight = ref(false);
      let weight = ref('');
      let selectedExercise = ref({});

      const store = useStore();

      const route = useRoute();
      const showWeightModal = (exercise) => {
        selectedExercise.value = exercise;
        weightModalVisible.value = true;

        weight.value = exercise.weight;
      };

      const saveWeight = (exercise) => {
        savingWeight.value = true;
        exercise.weight = weight.value;

        store.dispatch('workout/updateWorkoutWeight', {
          day: parseInt(route.params.id),
          exercise: exercise.id,
          weight: exercise.weight,
        })
          .then(() => {
            weightModalVisible.value = false;
            savingWeight.value = false;
          });
      };

      const workout = computed(() => store.getters['workout/workout']);
      let loading = ref(false);
      onMounted(() => {
        loading.value = true;
        store.dispatch('workout/getWorkoutDay', route.params.id)
          .then(_ => {
            loading.value = false;
          });
      });
      const tableHeight = computed(() => {
        let body = document.body;
        let html = document.documentElement;

        let height = Math.max(
          body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight, html.offsetHeight,
        );

        return `${height - 230}px`;
      });
      const isMobile = computed(() => {
        let windowWidth = window.screen.width < window.outerWidth ?
          window.screen.width : window.outerWidth;

        return windowWidth < 768;
      });

      return {
        workout,
        weightModalVisible,
        weight,
        selectedExercise,

        formLabelWidth: '120px',

        showWeightModal,
        saveWeight,
        savingWeight,
        tableHeight,
        isMobile,

        loading,
      };
    },
  };
</script>