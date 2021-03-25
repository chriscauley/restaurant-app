import Api from './Api'
import router from '@/router'

const api = Api()

const fetch = () => api.get('cart/')

const addItem = item_id => api.post('cart/add/', { item_id })

const removeItem = item_id => api.post('cart/remove/', { item_id })

const checkout = () => {
  api.post('cart/checkout/').then(({ order_id }) => {
    router.push({ name: 'orderdetail', params: { order_id } })
  })
}

export default { fetch, addItem, removeItem, checkout }
