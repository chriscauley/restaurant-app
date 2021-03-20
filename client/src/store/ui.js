import { reactive } from 'vue'

let ID_COUNTER = 0
const DELAY = 10000

const state = reactive({
  alert: null,
  toasts: [],
})

const hide = id => {
  const item = state.toasts.find(item => item.id === id)
  item.hidden = true
}

export default {
  alert: item => (state.alert = item),
  closeAlert: () => (state.alert = null),
  toast: item => {
    const id = ID_COUNTER++
    item.id = id
    item.hidden = false
    state.toasts.push(item)
    setTimeout(() => hide(item.id), DELAY)
  },
  state,
}
