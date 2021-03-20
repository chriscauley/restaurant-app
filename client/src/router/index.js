import { defaultsDeep } from 'lodash'
import { createRouter, createWebHistory } from 'vue-router'

import applyMeta from './applyMeta'
import checkAuth from './checkAuth'
import checkRole from './checkRole'
import views from '@/views'

const routes = []

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

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(applyMeta)
router.beforeEach(checkAuth)
router.beforeEach(checkRole)

export default router
