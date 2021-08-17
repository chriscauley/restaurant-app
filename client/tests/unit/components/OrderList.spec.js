import { shallowMount } from '@vue/test-utils'

import OrderList from '@/components/OrderList'

const getOptions = (role) => ({
  mocks: {
    $store: {
      auth: {
        get: () => ({ role }),
      },
    },
  },
})

const newOrder = (status, total_items, allowed_status) => ({
  user_name: 'username',
  created: '2020-01-01',
  total_price: 10,
  status,
  total_items,
  allowed_status,
})

const order1 = newOrder('canceled', 1)
const order2 = newOrder('pending', 2, 'canceled')
const order3 = newOrder('pending', 3)

test('OrderList methods: user role', () => {
  // Because everything is rendered inside of <router-links> none of this appears in wrapper.text()
  const propsData = {
    orders: [order1, order3],
  }

  const wrapper = shallowMount(OrderList, { propsData, global: getOptions('user') })
  expect(wrapper.vm.is_owner).toBe(false)
  expect(wrapper.vm.getDate(order1)).toBe('Jan 1, 2020')
  expect(wrapper.vm.getDescription(order1)).toBe('You ordered 1 item')
})

test('OrderList methods: owner role', () => {
  // Because everything is rendered inside of <router-links> none of this appears in wrapper.text()
  const propsData = {
    orders: [order3],
  }

  const wrapper = shallowMount(OrderList, { propsData, global: getOptions('owner') })
  expect(wrapper.vm.is_owner).toBe(true)
  expect(wrapper.vm.getDate(order3)).toBe('Jan 1, 2020')
  expect(wrapper.vm.getDescription(order3)).toBe('username ordered 3 items')
})

test('OrderList methods: statuses', () => {
  // Because everything is rendered inside of <router-links> none of this appears in wrapper.text()
  const propsData = {
    orders: [order1, order2, order3],
  }

  const wrapper = shallowMount(OrderList, { propsData, global: getOptions('owner') })
  expect(wrapper.vm.getStatusClass(order1)[1]).toBe('-danger')
  expect(wrapper.vm.getStatusClass(order2)[1]).toBe('-primary')
  expect(wrapper.vm.getStatusClass(order3)[1]).toBe('-secondary')
})
