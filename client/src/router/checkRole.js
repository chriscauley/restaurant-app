import store from '@/store'

const requireRole = (role, to, next) => {
  if (store.auth.get()?.role !== role) {
    store.ui.toast({ text: `Only ${role} users can view that page`, level: 'danger' })
    next({ path: '/' })
  } else {
    next()
  }
}

export default (to, from, next) => {
  const requiredRole = to.matched.map(record => record.meta.requiredRole).find(role => role)
  if (requiredRole) {
    store.auth.check().then(() => requireRole(requiredRole, to, next))
  } else {
    next()
  }
}
