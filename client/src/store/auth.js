import { reactive } from 'vue'
import api from '@/common/api'

const pending = []

const state = reactive({
  user: null,
  loading: null,
  loaded: null,
})

const logout = () =>
  api.post('logout').then(() => {
    state.user = null
    check()
  })

const check = async () => {
  if (state.loading) {
    return new Promise(resolve => pending.push(resolve))
  }
  if (!state.loaded) {
    state.loading = true
    return api.get('whoami').then(({ user }) => {
      state.user = user
      state.loading = false
      state.loaded = true
      while (pending.length) {
        // resolve any other pending promises
        pending.pop()()
      }
    })
  }
}

export default {
  state,
  check,
  init: check,
  logout,
}
