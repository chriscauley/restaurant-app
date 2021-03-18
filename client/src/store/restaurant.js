import { reactive } from 'vue'
import api from '@/common/api'
import slugify from '@/common/slugify'

const DEFAULT_IMG = '/static/pizza.png'

const state = reactive({
  by_id: {},
  with_menu: {},
})

const setRestaurant = data => {
  state.by_id[data.id] = {
    ...state[data.id],
    ...data,
    img_style: `background-image: url(${data.photo_url || DEFAULT_IMG})`,
    to: `/restaurant/${data.id}/${slugify(data.name)}/`,
  }
}

const fetch = (page = 1) => {
  api.get('restaurant/?page=' + page).then(({ items }) => items.forEach(setRestaurant))
}

const fetchmenu = id => {
  if (!state.by_id[id]?.menusections) {
    api.get(`restaurant/${id}/`).then(setRestaurant)
  }
  return state.by_id[id]
}

const init = fetch

const all = () => Object.values(state.by_id)
export default { state, fetch, fetchmenu, init, all }
