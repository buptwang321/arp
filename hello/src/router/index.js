import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Admin from '../components/Admin'
import Login from '../components/Login'
import Label from '../components/Label'
import Advertisers from '../components/Advertisers'
import Platforms from '../components/Platforms'
import Add_ads from '../components/Add_ads'
import Get_ads from '../components/Get_ads'
import Show_users from '../components/Show_users'
import Add_cust from '../components/Add_cust'
import Show_cust from '../components/Show_cust'
import Show_recommend from '../components/Show_recommend'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
   {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/admin',
    name: 'admin',
    component: Admin,
    children: [
      {
        path: 'label',
        name: 'label',
        component: Label
      },
      {
        path: 'get_ads',
        name: 'get_ads',
        component: Get_ads
      },
      {
        path: 'show_users',
        name: 'show_users',
        component: Show_users
      },
      {
        path: 'show_cust',
        name: 'show_cust',
        component: Show_cust
      }
    ]
  },
  {
    path: '/advertisers',
    name: 'advertisers',
    component: Advertisers,
    children: [
      {
        path: 'add_ads',
        name: 'add_ads',
        component: Add_ads
      },
      {
        path: 'get_ads',
        name: 'get_ads',
        component: Get_ads
      }
    ]
  },
  {
    path: '/platforms',
    name: 'platforms',
    component: Platforms,
    children: [
      {
        path: 'add_cust',
        name: 'add_cust',
        component: Add_cust
      },
      {
        path: 'show_cust',
        name: 'show_cust',
        component: Show_cust
      },
      {
        path: 'show_recommend',
        name: 'show_recommend',
        component: Show_recommend
      }
    ]
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
