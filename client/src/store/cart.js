import { reactive } from 'vue'
import api from '@/common/api'
import router from '@/router'

const state = reactive({
  restaurant_id: null,
  items: [],
})

const setState = data => Object.assign(state, data)

const fetch = () => api.get('cart/').then(setState)

const addItem = item_id => api.post('cart/add/', { item_id }).then(setState)

const removeItem = item_id => api.post('cart/remove/', { item_id }).then(setState)

const checkout = () => {
  api.post('cart/checkout/').then(({ order_id }) => {
    setState({ restaurant_id: null, items: [] })
    router.push({ name: 'orderdetail', params: { order_id } })
  })
}

export default { state, fetch, init: fetch, addItem, removeItem, checkout }
