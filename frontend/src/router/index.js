import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'
import { ClientTable } from 'vue-tables-2'

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/user', component: 'User' },
  { path: '/about', component: 'About' },
  { path: '/helloworld', component: 'HelloWorld' },
  { path: '/tryaccess/:accessType', component: 'TryAccess' },
  { path: '/musiclist', component: 'MusicList' },
  { path: '/musicupload', component: 'Upload' },
  { path: '/sing/:song_id', name: 'singmusic', component: 'Sing' },
  { path: '*', component: 'NotFound' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)
Vue.use(axios)
Vue.use(ClientTable)

export default new Router({
  routes,
  mode: 'hash'
})
