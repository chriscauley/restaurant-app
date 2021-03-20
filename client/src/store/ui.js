import { reactive } from 'vue'

let ID_COUNTER = 0
const DELAY = 5000

const state = reactive({
  alert: null,
  toasts: [],
})

export default {
  alert: item => (state.alert = item),
  closeAlert: () => (state.alert = null),
  toast: item => {
    const id = ID_COUNTER++
    item.id = id
    item.hidden = false
    state.toasts.push(item)
    console.log(state.toasts)
    setTimeout(() => (item.hidden = console.log('hide') || true), DELAY)
  },
  state,
}
