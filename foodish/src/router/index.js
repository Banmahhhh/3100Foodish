import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/home')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login')
    },
    {
      path: '/post',
      name: 'Post',
      component: () => import('@/views/post')
    },
    {
      path: '/info',
      name: 'Info',
      component: () => import('@/views/info')
    },
    {
      path: '/person',
      name: 'Person',
      component: () => import('@/views/person')
    },
    {
      path: '/personHome',
      name: 'PersonHome',
      component: () => import('@/views/personHome')
    }
  ]
})
let filter = ['Login']

router.beforeEach(function(to, from, next){
  let users = window.localStorage.getItem('users')||""
  if(to.name==='Login'){
    return next();
  }
  if (users.indexOf('id')!==-1) {
      return next();
  }
  next({ name:'Login'});
})
export default router
