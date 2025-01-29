import { createRouter, createWebHistory } from 'vue-router';
import NetflixTable from './components/NetflixTable.vue';
import DetailsView from './components/DetailsView.vue';

const routes = [
  { path: '/', component: NetflixTable },
  { path: '/:show_id', component: DetailsView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;