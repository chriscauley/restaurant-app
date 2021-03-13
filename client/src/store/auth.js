import { reactive } from 'vue'
import api from '@/common/api'

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

const check = () => {
  if (!state.user) {
    state.loading = true
    api.get('whoami').then(({ user }) => {
      state.user = user
      state.loading = false
      state.loaded = true
    })
  }
}

export default {
  state,
  check,
  init: check,
  logout,
}
