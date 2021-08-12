import auth from '@unrest/vue-auth'
import unrest from '@unrest/vue'

const requireRole = (role, to, next) => {
  if (auth.get()?.role !== role) {
    unrest.ui.toast({ text: `Only ${role} users can view that page`, level: 'danger' })
    next({ path: '/' })
  } else {
    next()
  }
}

export default (to, from, next) => {
  const requiredRole = to.matched.map(record => record.meta.requiredRole).find(role => role)
  if (requiredRole) {
    auth.fetch().then(() => requireRole(requiredRole, to, next))
  } else {
    next()
  }
}
