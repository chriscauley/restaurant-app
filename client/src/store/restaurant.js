import { reactive } from 'vue'
import api from '@/common/api'

const state = reactive({
  by_id: {},
})

const fetch = (page = 1) => {
  api.get('restaurant/?page=' + page).then(response => {
    response.items.forEach(restaurant => {
      state.by_id[restaurant.id] = restaurant
    })
  })
}

const init = fetch

export default { state, fetch, init, all: () => Object.values(state.by_id) }
