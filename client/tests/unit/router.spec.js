import checkAuth from '@/router/checkAuth'
import checkRole from '@/router/checkRole'
import { self_user } from '@tests/dummy'
import api from '@/common/api'
import store from '@/store'

jest.mock('@/common/api')

const dummyTo = {
  guest: {
    matched: [],
    params: {},
  },
  authRequired: {
    matched: [{ meta: { authRequired: true } }],
    params: {},
  },
  authRedirect: {
    matched: [{ meta: { authRedirect: true } }],
    params: {},
  },
  requireOwner: {
    matched: [{ meta: { requiredRole: 'owner' } }],
    params: {},
  }
}

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

test('checkAuth', async _next => {
  const authRequiredRedirect = {
    name: 'login',
    params: { next: undefined },
  }

  api._mock.get('self/', {})
  await store.auth.check()
  await doCheckAuth(dummyTo.guest, undefined)
  await doCheckAuth(dummyTo.authRequired, authRequiredRedirect)
  await doCheckAuth(dummyTo.authRedirect, undefined)

  api._mock.get('self/', self_user)
  await store.auth.refetch()
  await doCheckAuth(dummyTo.guest, undefined)
  await doCheckAuth(dummyTo.authRequired, undefined)
  await doCheckAuth(dummyTo.authRedirect, '/')

  api._mock.get('self/', {})
  await store.auth.refetch()
  _next()
})

console.log(self_user

test('checkRole', async _next => {
  
})