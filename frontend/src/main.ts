import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/login',
      component: () => import('./views/Login.vue')
    },
    {
      path: '/register',
      component: () => import('./views/Register.vue')
    },
    {
      path: '/profile',
      component: () => import('./views/Profile.vue')
    },
    {
      path: '/apply',
      component: () => import('./views/Apply.vue')
    }
  ]
});

// Create the Vue application
const app = createApp(App);
app.use(router);

// Mount the app
app.mount('#app');
