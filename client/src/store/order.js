import api from '@/common/api'
import { reactive } from 'vue'

const state = reactive({
  list: [],
  by_id: {},
})

const fetch = (id, force) => {
  if (!state.by_id[id] || force) {
    api.get(`order/${id}/`).then(d => (state.by_id[id] = d))
  }
  return state.by_id[id]
}

const cancel = order_id => {
  api.post(`order/${order_id}/`, { status: 'canceled' }).then(d => (state.by_id[order_id] = d))
}

export default { state, fetch, cancel }
