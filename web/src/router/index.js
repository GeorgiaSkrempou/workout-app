import {
    createRouter,
    createWebHistory,
} from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'public.home',
        component: () => import(/* webpackChunkName: 'about' */ '../views/Home.vue'),
    },
    {
        path: '/login',
        name: 'public.login',
        component: () => import(/* webpackChunkName: 'login' */ '../views/Login.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
