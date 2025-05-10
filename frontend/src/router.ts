import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Profile from './components/Profile.vue';
import Apply from './components/Apply.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', component: Login },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile },
  { path: '/apply', component: Apply }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
