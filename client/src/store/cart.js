import { ReactiveRestApi } from '@unrest/vue-reactive-storage'
import client from '@/common/api'
import router from '@/router'

const store = ReactiveRestApi({ client })

const fetch = () => store.fetch('cart/')
const get = () => store.get('cart/')

const addItem = item_id => store.post('cart/add/', { item_id }).then(fetch)

const removeItem = item_id => store.post('cart/remove/', { item_id }).then(fetch)

const checkout = () => {
  store.post('cart/checkout/').then(({ order_id }) => {
    router.push({ name: 'orderdetail', params: { order_id } })
  })
}

export default { get, fetch, addItem, removeItem, checkout }
