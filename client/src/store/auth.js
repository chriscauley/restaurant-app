import Api from './Api'

const api = Api()

const check = () => new Promise(resolve => api.get('self/', resolve))
const get = () => api.get('self/')?.user

const logout = () => api.post('logout/').then(refetch)

const refetch = () => {
  api.markStale()
  return new Promise(resolve => api.get('self/', resolve))
}

export default {
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
