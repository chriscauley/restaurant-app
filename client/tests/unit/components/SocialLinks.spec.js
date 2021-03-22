import { shallowMount } from '@vue/test-utils'

import SocialLinks from '@/components/SocialLinks'

test('SocialLinks', () => {
  const propsData = {
    verb: 'Foo',
  }

  const wrapper = shallowMount(SocialLinks, { propsData })
  expect(wrapper.text()).toBe('Or Foo With Twitter Github')
})
