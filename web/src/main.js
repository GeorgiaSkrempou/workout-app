import 'element-plus/dist/index.css';
import { createApp } from 'vue';
import App from './App.vue';
import './assets/scss/app.scss';
import { router } from './router';
import { store } from './store';

import { ElInfiniteScroll } from 'element-plus';

const app = createApp(App);

app.use(router);
app.use(store);

app.use(ElInfiniteScroll);

app.mount('#app');
