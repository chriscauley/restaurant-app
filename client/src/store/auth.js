import { ReactiveRestApi } from '@unrest/vue-reactive-storage'

import api from '@/common/api'

const URL = 'self/'
const store = ReactiveRestApi({ client: api })
const get = () => store.get(URL)?.user
const check = () => store.fetch(URL).then(r => r.user)

export default {
  get,
  check,
  logout: () => store.post('logout/').then(get),
  refetch: () => {
    store.markStale()
    return check()
  },
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
