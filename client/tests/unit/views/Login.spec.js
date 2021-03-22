import { shallowMount } from '@vue/test-utils'
import Login from '@/views/Login'

test('Login', next => {
  const wrapper = shallowMount(Login, {})
  expect(wrapper.text()).toBe('')
  next()
})
