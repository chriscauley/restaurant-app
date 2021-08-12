import { defaultsDeep } from 'lodash'
import { createRouter, createWebHistory, createMemoryHistory } from 'vue-router'
import auth from '@unrest/vue-auth'

import applyMeta from './applyMeta'
import checkRole from './checkRole'
import store from '@/store'
import views from '@/views'

const routes = [...auth.routes]

const loadViews = o =>
  Object.entries(o).forEach(([component_name, Component]) => {
    const route = {
      name: component_name.toLowerCase(),
      path: `/${component_name.toLowerCase()}`,
      component: Component,
    }
    Object.assign(route, Component.__route)
    defaultsDeep(route, { meta: { title: component_name } })
    routes.push(route)
  })

loadViews(views)
const createHistory = process.env.NODE_ENV === 'test' ? createMemoryHistory : createWebHistory

const router = createRouter({
  history: createHistory(),
  routes,
})

router.beforeEach(applyMeta)
router.beforeEach(checkRole)
router.beforeEach(() => {
  // refresh any api calls after navigation
  store.restaurant.api.markStale()
  store.order.api.markStale()
})
export default router
