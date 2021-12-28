import axios from 'axios';

const defaultWorkoutState = () => {
  return {
    workouts: [],
    workout: {},
    workoutLoaded: false,
    workoutsLoaded: false,
  };
};

const state = defaultWorkoutState();

const getters = {
  workouts: (state) => state.workouts,
  workout: (state) => state.workout,
  workoutLoaded: (state) => state.workoutLoaded,
  workoutsLoaded: (state) => state.workoutsLoaded,
};

const mutations = {
  setWorkouts: (state, payload) => {
    state.workouts = payload;
  },
  setWorkout: (state, payload) => {
    state.workout = payload;
    state.workoutLoaded = true;
  },
  setWorkoutsLoaded: (state, payload) => {
    state.workoutsLoaded = payload;
  },
  resetWorkoutStore: (state) => {
    Object.assign(state, defaultWorkoutState());
  },
};

const actions = {
  getAll: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/user/workouts/${localStorage.getItem('user')}`,
        method: 'GET',
      })
        .then((response) => {
          commit('setWorkouts', response.data);
          commit('setWorkoutsLoaded', true);

          resolve(response);
        })
        .catch(error => reject(error.response.data));
    });
  },
  getWorkoutDay: ({ commit }, day) => {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/user/workouts/${localStorage.getItem('user')}/day${day}`,
        method: 'GET',
      })
        .then((response) => {
          commit('setWorkout', response.data);

          resolve(response);
        })
        .catch(error => reject(error.response.data));
    });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};