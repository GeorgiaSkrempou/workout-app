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
        </h4>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table
          v-loading='loading'
          :data='exercises'
          @current-change='showWeightModal'
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
          <el-table-column
            label='Weight'
            prop='weight'
          />
        </el-table>
      </el-col>
    </el-row>

    <el-dialog
      v-model='weightModalVisible'
      :title='`Update weight for ${selectedExercise.name}`'
      destroy-on-close
      width='25%'
    >
      <el-form>
        <el-form-item
          :label-width='formLabelWidth'
          label='Weight'>
          <el-input
            v-model='weight'
            autocomplete='off'
            autofocus
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
    ElTable,
    ElTableColumn,
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

      ArrowLeftBold,
    },
    setup() {
      let weightModalVisible = ref(false);
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
        exercise.weight = weight.value;
        weightModalVisible.value = false;
      };

      const exercises = computed(() => store.getters['workout/workout']);
      let loading = ref(false);
      onMounted(() => {
        loading.value = true;
        store.dispatch('workout/getWorkoutDay', route.params.id)
          .then(_ => {
            loading.value = false;
          });
      });

      return {
        exercises,
        weightModalVisible,
        weight,
        selectedExercise,

        formLabelWidth: '120px',

        showWeightModal,
        saveWeight,

        loading,
      };
    },
  };
</script>