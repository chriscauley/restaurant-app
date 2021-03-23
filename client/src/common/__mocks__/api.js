const store = {}
const _mock = (url, data, prefix = '') => {
  const key = prefix + url
  // console.log('mocking', key)
  if (store[key]) {
    throw `Attempted to overload stored data for: ` + key
  }
  store[key] = data
}
const _get = (url, prefix = '') => {
  const key = prefix + url
  // console.log('mocked', key)
  const data = store[key]
  delete store[key]
  return new Promise((resolve, reject) => {
    if (data.throw) {
      reject(data.throw)
    } else {
      resolve(data === 'NULL' ? null : data)
    }
  })
}

export default {
  _mock: {
    get: (url, data) => _mock(url, data),
    post: (url, data) => _mock(url, data, 'POST:'),
    cleanUp: () => expect(Object.keys(store)).toStrictEqual([]), // eslint-disable-line
  },
  get: url => _get(url),
  post: url => _get(url, 'POST:'),
}
