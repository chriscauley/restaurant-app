import checkAuth from '@/router/checkAuth'
import checkRole from '@/router/checkRole'
import { self_user } from '@tests/dummy'
import store from '@/store'

jest.mock('@/common/api')

const dummyTo = {
  guest: {
    matched: [],
    params: {},
    query: {},
  },
  authRequired: {
    matched: [{ meta: { authRequired: true } }],
    params: {},
    query: {},
  },
  authRedirect: {
    matched: [{ meta: { authRedirect: true } }],
    params: {},
    query: {},
  },
  requireUserRole: {
    matched: [{ meta: { requiredRole: 'user' } }],
    params: {},
    query: {},
  },
}

test('checkAuth', async _next => {
  const doCheckAuth = (to, expectedLocation) => {
    let resolve
    const promise = new Promise(r => (resolve = r))
    const next = location => {
      expect(location).toStrictEqual(expectedLocation)
      resolve()
    }
    checkAuth(to, null, next)
    return promise
  }

  const authRequiredRedirect = {
    name: 'login',
    query: { next: undefined },
  }

  store.auth.setFaked(self_user.user)
  await doCheckAuth(dummyTo.guest, undefined)
  await doCheckAuth(dummyTo.authRequired, undefined)
  await doCheckAuth(dummyTo.authRedirect, '/')

  store.auth.setFaked(null)
  await doCheckAuth(dummyTo.guest, undefined)
  await doCheckAuth(dummyTo.authRequired, authRequiredRedirect)
  await doCheckAuth(dummyTo.authRedirect, undefined)

  store.auth.setFaked(undefined)
  _next()
})

test('checkRole', async _next => {
  const old_toast = store.ui.toast
  store.ui.toast = jest.fn()

  const doCheckRole = (to, expectedLocation) => {
    let resolve
    const promise = new Promise(r => (resolve = r))
    const next = location => {
      expect(location).toStrictEqual(expectedLocation)
      resolve()
    }
    checkRole(to, null, next)
    return promise
  }

  store.auth.setFaked(self_user.user)
  await doCheckRole(dummyTo.guest, undefined)
  await doCheckRole(dummyTo.requireUserRole, undefined)

  store.auth.setFaked(null)
  await doCheckRole(dummyTo.guest, undefined)

  // redirect calls toast
  expect(store.ui.toast).toHaveBeenCalledTimes(0)
  await doCheckRole(dummyTo.requireUserRole, { path: '/' })
  expect(store.ui.toast).toHaveBeenCalled()

  store.auth.setFaked(undefined)
  store.ui.toast = old_toast
  _next()
})
