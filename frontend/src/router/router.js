import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import FundPosition from '../pages/FundPosition.vue';
import Market from '../pages/Market.vue';
import Percentile from '../pages/Percentile.vue';

const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: MainPage
    },
    {
        path: '/position',
        name: 'FundPosition',
        component: FundPosition
    },
    {
        path: '/market',
        name: 'Market',
        component: Market
    },
    {
        path: '/percentile',
        name: 'Percentile',
        component: Percentile
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;