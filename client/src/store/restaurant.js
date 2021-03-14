import { reactive } from 'vue'
import api from '@/common/api'
import slugify from '@/common/slugify'

const state = reactive({
  by_id: {},
})

const fetch = (page = 1) => {
  api.get('restaurant/?page=' + page).then(response => {
    response.items.forEach(restaurant => {
      state.by_id[restaurant.id] = {
        img_style: `background-image: url(${restaurant.photo_url})`,
        to: `/restaurant/${restaurant.id}/${slugify(restaurant.name)}/`,
        ...restaurant,
      }
    })
  })
}

const init = fetch

export default { state, fetch, init, all: () => Object.values(state.by_id) }
