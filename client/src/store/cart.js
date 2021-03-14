import { reactive } from 'vue'
import api from '@/common/api'

const state = reactive({
  restaurant_id: null,
  items: [],
})

const setState = data => Object.assign(state, data)

const fetch = () => api.get('cart/').then(setState)

const addItem = item_id => api.post('cart/add/', { item_id }).then(setState)

const removeItem = item_id => api.post('cart/remove/', { item_id }).then(setState)

export default { state, fetch, init: fetch, addItem, removeItem }
