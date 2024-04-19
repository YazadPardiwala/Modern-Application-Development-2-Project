import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login_pg from '../views/Login_pg.vue'
import Signup_pg from '../views/Signup_pg.vue'

import Future_shows from '../views/Future_airings.vue'
import Booked_shows from '../views/Booked_airings.vue'

import Maketheatre_form from '../components/Maketheatre_form.vue'
import Your_theatres from '../views/Your_theatres.vue'
import Modtheatre_form from '../components/Modtheatre_form.vue'
import All_theatres from '../views/All_theatres.vue'

import Makeshow_form from '../components/Makeshow_form.vue'
import Your_shows from '../views/Your_shows.vue'
import Modshow_form from '../components/Modshow_form.vue'
import Show_book_form from '../components/Show_book_form.vue'
import All_shows from '../views/All_shows.vue'
import Rateshow_form from '../components/Rateshow_form.vue'

import Makeairing_form from '../components/Makeairing_form.vue'
import Modairing_form from '../components/Modairing_form.vue'
import Your_airings from '../views/Your_airings.vue'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
      path: '/',
      name: 'Login_pg',
      component: Login_pg
  },
  {
      path: '/sign_up',
      name: 'Signup_pg',
      component: Signup_pg
  },

  {
      path: '/Future_shows',
      name:'Future_shows',
      component: Future_shows
  },
  {
      path: '/Booked_shows',
      name: 'Booked_shows',
      component: Booked_shows
  },

  {
      path: '/All_theatres',
      name:'All_theatres',
      component:All_theatres
  },
  {
      path:'/Your_theatres',
      name:'Your_theatres',
      component: Your_theatres
  },
  {
      path:'/Maketheatre',
      name: 'Maketheatre_form',
      component: Maketheatre_form
  },
  {
      path:'/Modtheatre/:TID/:ACTION',
      name:'Modtheatre_form',
      component:Modtheatre_form
  },

  {
      path:'/Show_book/:AID',
      name:'Show_book_form',
      component: Show_book_form
  },
  {
      path: '/Your_shows',
      name: 'Your_shows',
      component: Your_shows
  },
  {
      path:'/All_shows',
      name:'All_shows',
      component: All_shows
  },
  {
      path:'/Makeshow',
      name:'Makeshow_form',
      component:Makeshow_form
  },
  {
      path:'/Modshow/:SID/:ACTION',
      name:'Modshow_form',
      component:Modshow_form
  },
  {
      path:'/Rateshow/:show_list/:index',
      name:'Rateshow_form',
      component:Rateshow_form
  },

  {
      path:'/Makeairing_form',
      name:'Makeairing_form',
      component:Makeairing_form
  },
  {
      path:'/Modairing_form/:INDEX/:ACTION',
      name:'Modairing_form',
      component:Modairing_form
  },
  {
      path:'/Your_airings',
      name:'Your_airings',
      component:Your_airings
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
