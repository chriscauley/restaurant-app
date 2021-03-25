import Api from '@/store/Api'
import api from '@/common/api'

const { _mock } = api

jest.mock('@/common/api')

test.skip('Api', async next => {
  let resolve
  const url = 'URL'
  const api = Api()

  // Api.prototype.get returns nothing at first
  const promise = new Promise(r => (resolve = r))
  _mock.get(url, { foo: 'bar' })
  const first_result = api.get(url, resolve)
  expect(first_result).toBe(undefined)

  // it then returns result of _mock.get() after next resolves
  await promise
  const second_result = api.get(url)
  expect(second_result.foo).toBe('bar')

  // calling get again returns the same result (does not make another call)
  _mock.get(url, { foo: 'updated' })
  const promise2 = new Promise(r => (resolve = r))
  const third_result = api.get(url, resolve)
  await promise2
  expect(third_result.foo).toBe('bar')

  // after marking stale, calling api.get again gives new result
  // TODO this is failing intermittently
  api.markStale()
  const promise3 = new Promise(r => (resolve = r))
  api.get(url, resolve)
  await promise3
  expect(api.get(url)).toStrictEqual({ foo: 'updated' })

  next()
})
