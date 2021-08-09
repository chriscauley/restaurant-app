import { shallowMount } from '@vue/test-utils'

import Modal from '@/components/Modal'

test('Modal', next => {
  const propsData = {
    title: 'My Title',
    close: jest.fn(),
  }

  const wrapper = shallowMount(Modal, { propsData })
  expect(wrapper.text()).toBe(propsData.title + 'Close')
  wrapper.find('.modal-mask').trigger('click')
  wrapper.find('.modal-footer button').trigger('click')
  expect(propsData.close.mock.results.length).toBe(2)
  next()
})
