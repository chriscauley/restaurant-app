import { ReactiveRestApi } from '@unrest/vue-storage'
import client from '@/common/api'
import router from '@/router'
import uS from '@unrest/story'

const complete = action => data => {
  uS.complete(`customer.${action}`)
  return fetch(data)
}

const store = ReactiveRestApi({ client })

const fetch = () => store.fetch('cart/')
const get = () => store.get('cart/')

const addItem = item_id => store.post('cart/add/', { item_id }).then(complete('createCartItem'))

const removeItem = item_id =>
  store.post('cart/remove/', { item_id }).then(complete('removeCartItem'))

const checkout = () => {
  store.post('cart/checkout/').then(({ order_id }) => {
    uS.complete('customer.placeOrder')
    router.push({ name: 'orderdetail', params: { order_id } })
  })
}

export default { get, fetch, addItem, removeItem, checkout }
