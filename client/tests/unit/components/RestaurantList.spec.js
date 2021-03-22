import { shallowMount } from '@vue/test-utils'

import RestaurantList from '@/components/RestaurantList'
import { getRestaurantPage } from '@tests/dummy'

test('RestaurantList', next => {
  const count = 12
  const restaurants = getRestaurantPage({ count }).items
  const wrapper = shallowMount(RestaurantList, { propsData: { restaurants } })
  expect(wrapper.findAll('router-link-stub').length).toBe(count)
  expect(wrapper.text()).toBe('')
  next()
})
