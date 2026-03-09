import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '../pages/Home.vue'
import About from '../pages/About.vue'
import Camera from '../pages/CameraPage.vue'
import List from '../pages/List.vue'
import Result from '../pages/Result.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/camera',
    name: 'Camera',
    component: Camera,
  },
  {
    path: '/list',
    name: 'List',
    component: List,
  },
  {
    path: '/result',
    name: 'Result',
    component: Result,
  },
]

export const router = createRouter({
  history: createWebHashHistory(), // <--- TO THIS
  routes,
})