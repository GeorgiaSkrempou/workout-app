import 'element-plus/dist/index.css';

import { createApp } from 'vue';
import App from './App.vue';
import './assets/scss/app.scss';
import { http } from './providers/http';
import { router } from './router';
import { store } from './store';

import { ElLoading } from 'element-plus';
import { ElInfiniteScroll } from 'element-plus';


http.mount();

const app = createApp(App);

app.use(router);
app.use(store);

app.use(ElInfiniteScroll);
app.use(ElLoading);

app.mount('#app');
