import store from '@/store'
import { self_user } from '@tests/dummy'
import api from '@/common/api'

jest.mock('@/common/api')

test.skip('store.auth login/logout flow', async (done) => {
  api._mock.get('self/', self_user)
  await store.auth.check()
  expect(store.auth.get().username).toBe('user')
  api._mock.get('logout/', {})
  api._mock.post('logout/', {})
  api._mock.get('self/', {})
  await store.auth.logout()
  expect(store.auth.get()).toBe(undefined)
  api._mock.cleanUp()
  setTimeout(done, 100)
})
