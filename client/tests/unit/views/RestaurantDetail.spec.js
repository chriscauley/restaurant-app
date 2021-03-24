import { shallowMount } from '@vue/test-utils'
import { reactive } from 'vue'

import RestaurantDetail from '@/views/RestaurantDetail'

const mockStore = restaurant => {
  const findItem = id => {
    let item
    restaurant.menusections.forEach(menusection => {
      item = item || menusection.items.find(item2 => item2.id === id)
    })
    return item
  }
  const $store = {
    restaurant: {
      markStale: jest.fn(),
      fetchOne: jest.fn(() => restaurant),
    },
    cart: {
      state: reactive({
        items: [],
      }),
      addItem: _item_id => {
        const item = findItem(_item_id)
        $store.cart.state.items.push({ quantity: 1, price: item.price, _item_id })
      },
      removeItem: _item_id => {
        $store.cart.state.items = $store.cart.state.items.filter(item => item._item_id !== _item_id)
      },
      checkout: jest.fn(),
    },
  }
  return $store
}

const mountElement = restaurant => {
  const $store = mockStore(restaurant)
  return shallowMount(RestaurantDetail, {
    global: {
      mocks: {
        $route: { params: {} },
        $store,
      },
    },
  })
}

const poke_bowls = {
  id: 275,
  name: 'Poke Bowls',
  items: [
    {
      id: 1,
      name: 'Yuzu Salmon',
      price: 10,
      description: 'None',
    },
  ],
}

test('RestaurantDetail renders properly', () => {
  const wrapper = mountElement({
    name: 'My restaurant',
    menusections: [poke_bowls],
  })

  expect(wrapper.find('h1').text()).toBe('My restaurant')
  expect(wrapper.find('.cart-total').text()).toBe('$0')
  expect(wrapper.find('.menu-section h2').text()).toBe('Poke Bowls')
  expect(wrapper.find('.menu-item__name').text()).toBe('Yuzu Salmon')
})

test('RestaurantDetail cart functions properly', () => {
  const wrapper = mountElement({
    name: 'My restaurant',
    menusections: [poke_bowls],
  })

  wrapper.vm.addItem(1)
  expect(wrapper.vm.total).toBe(10)
  wrapper.vm.removeItem(1)
  expect(wrapper.vm.total).toBe(0)
  wrapper.vm.checkout()
  expect(wrapper.vm.$store.cart.checkout).toHaveBeenCalled()
})

test('RestaurantDetail owner can trigger edit modes', () => {
  const wrapper = mountElement({
    is_owner: true,
  })

  expect(wrapper.text().includes('Add another menu section')).toBe(true)

  wrapper.vm.addMenuSection()
  expect(wrapper.vm.form_name).toBe('menusection')

  wrapper.vm.addMenuItem({ id: 1 })
  expect(wrapper.vm.form_name).toBe('menuitem')

  wrapper.vm.edit('foo', 1)
  expect(wrapper.vm.form_name).toBe('foo/1')
})
