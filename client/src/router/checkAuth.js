import store from '@/store'

const requireAuth = (to, next) => {
  if (!store.auth.get()) {
    next({
      name: 'login',
      params: { next: to.fullPath },
    })
  } else {
    next()
  }
}

const redirectIfAuthed = (to, next) => {
  if (store.auth.get()) {
    next(to.params.next || '/')
  } else {
    next()
  }
}

export default (to, from, next) => {
  if (to.matched.some(record => record.meta.authRequired)) {
    store.auth.check().then(() => requireAuth(to, next))
  } else if (to.matched.some(record => record.meta.authRedirect)) {
    store.auth.check().then(() => redirectIfAuthed(to, next))
  } else {
    next()
  }
}
