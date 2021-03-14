import { reactive } from 'vue'
import api from '@/common/api'

const state = reactive({
  restaurant_id: null,
  items: [],
})

const setState = data => Object.assign(state, data)

const fetch = () => api.get('cart/').then(setState)

const addItem = ({ id }) => api.post('cart/add/', { item_id: id }).then(setState)

const removeItem = ({ id }) => api.post('cart/remove/', { item_id: id }).then(setState)

export default { state, fetch, init: fetch, addItem, removeItem }
