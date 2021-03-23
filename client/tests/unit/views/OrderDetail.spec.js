import { shallowMount } from '@vue/test-utils'
import { reactive } from 'vue'

import OrderDetail from '@/views/OrderDetail'

const mockOrderStore = () => {
  const state = reactive({
    order: newOrder(),
  })
  const $store = {
    order: {
      markStale: jest.fn(),
      fetchOne: jest.fn(() => {
        // got to modify the reactive element to trigger reflow
        if ($store._order) {
          state.order = $store._order
          delete $store._order
        }
        return state.order
      }),
      updateStatus: jest.fn(),
      blockUser: jest.fn(),
      unblockUser: jest.fn(),
    },
  }
  return $store
}

const wait = s =>
  new Promise(resolve => {
    setTimeout(resolve, s * 1000)
  })

const newOrder = data => ({
  created: new Date(),
  status_history: [{ status: 'placed', created: new Date() }],
  ...data,
})

const mountElement = (propsData = {}) => {
  const order_id = 1
  const $store = mockOrderStore()
  return shallowMount(OrderDetail, {
    propsData,
    global: {
      mocks: {
        $route: { params: { order_id } },
        $store,
      },
    },
  })
}

test('OrderDetail renders properly', () => {
  const wrapper = mountElement()

  expect(wrapper.find('h2').text()).toBe('You ordered from  less than a minute ago')
  expect(wrapper.find('.order-history').text()).toBe('placed less than a minute ago')
})

test('OrderDetail polls correctly', async next => {
  const POLL_FREQUENCY = 0.1
  const wrapper = mountElement({ POLL_FREQUENCY })

  wrapper.vm.$store._order = newOrder({ allowed_status: 'canceled', status: 'placed' })
  await wait(POLL_FREQUENCY * 2)

  wrapper.find('.btn-cancel').trigger('click')
  expect(wrapper.text().includes('Cancel Order')).toBe(true)
  expect(wrapper.vm.cancelling).toBe(true)

  wrapper.vm.$store._order = newOrder({ status: 'canceled' })
  await wait(POLL_FREQUENCY * 2)

  // prevent further timeouts
  wrapper.unmount()
  next()
})

test('OrderDetail calls store methods', () => {
  const wrapper = mountElement()

  wrapper.vm.confirmCancel()
  expect(wrapper.vm.$store.order.updateStatus).toHaveBeenCalled()

  wrapper.vm.$store.order.updateStatus.mockClear()
  wrapper.vm.markAllowedStatus()
  expect(wrapper.vm.$store.order.updateStatus).toHaveBeenCalled()

  wrapper.vm.blockUser()
  expect(wrapper.vm.$store.order.blockUser).toHaveBeenCalled()

  wrapper.vm.unblockUser()
  expect(wrapper.vm.$store.order.unblockUser).toHaveBeenCalled()
})
