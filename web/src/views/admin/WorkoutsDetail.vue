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
      width='25%'
      destroy-on-close
    >
      <el-form>
        <el-form-item
          label='Weight'
          :label-width='formLabelWidth'>
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
    ElIcon,
    ElRow,
    ElTable,
    ElTableColumn,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput,
  } from 'element-plus';
  import { ref } from 'vue';

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

      return {
        workout: workouts.find(el => el.id === parseInt(route.params.id)),
        exercises: exercises,
        weightModalVisible,
        weight,
        selectedExercise,

        formLabelWidth: '120px',

        showWeightModal,
        saveWeight,
      };
    },
  };
</script>