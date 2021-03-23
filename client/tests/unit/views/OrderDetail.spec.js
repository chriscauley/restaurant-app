import { shallowMount } from '@vue/test-utils'

import OrderDetail from '@/views/OrderDetail'
import api from '@/common/api'

jest.mock('@/common/api')

const order_id = 1
const order = {
  created: new Date(),
  status_history: [{ status: 'placed', created: new Date() }],
}

test('OrderDetail loads schema via api', async next => {
  api._mock.get(`order/${order_id}/`, order)

  const wrapper = shallowMount(OrderDetail, {
    global: { mocks: { $route: { params: { order_id } } } },
  })
  await Promise.resolve()
  expect(wrapper.find('h2').text()).toBe('You ordered from  less than a minute ago')
  expect(wrapper.find('.order-history').text()).toBe('placed less than a minute ago')

  api._mock.cleanUp()
  next()
})
