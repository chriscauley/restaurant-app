import { reactive } from 'vue'
import api from '@/common/api'

const pending = []

const state = reactive({
  user: null,
  loading: null,
  loaded: null,
})

const check = () => {
  if (state.loading) {
    return new Promise(resolve => pending.push(resolve))
  }
  if (!state.loaded) {
    state.loading = true
    return api.get('self/').then(({ user }) => {
      state.user = user
      state.loading = false
      state.loaded = true
      while (pending.length) {
        // resolve any other pending promises
        pending.pop()()
      }
    })
  }
  return Promise.resolve()
}

const logout = () => api.post('logout/').then(refetch)

const refetch = () => {
  state.loaded = state.loading = false
  return check()
}

export default {
  state,
  check,
  refetch,
  init: check,
  logout,
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
