import Api from './Api'

const api = Api()

let faked

const check = () => {
  if (faked !== undefined) {
    return Promise.resolve()
  }
  return new Promise(resolve => api.get('self/', resolve))
}

const get = () => {
  return faked !== undefined ? faked : api.get('self/')?.user
}

const logout = () => api.post('logout/').then(refetch)

const refetch = () => {
  api.markStale()
  return new Promise(resolve => api.get('self/', resolve))
}

export default {
  setFaked: user => (faked = user),
  check,
  refetch,
  logout,
  get,
  social: [
    {
      name: 'Twitter',
      slug: 'twitter',
      href: '/login/twitter/',
    },
    {
      name: 'Github',
      slug: 'github',
      href: '/login/github/',
    },
  ],
}
