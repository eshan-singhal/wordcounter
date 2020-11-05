import Vue from 'vue';
import Router from 'vue-router';
import Words from './components/Words.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Words',
      component: Words,
    }
  ],
});
