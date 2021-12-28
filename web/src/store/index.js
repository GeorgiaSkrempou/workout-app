import { createStore } from 'vuex';
import user from './modules/user';
import workout from './modules/workout';

export const store = createStore({
  modules: {
    user,
    workout,
  },
});
