import { shallowMount } from '@vue/test-utils'

import { RegistrationInvalid, RegistrationComplete } from '@/views/Registration'

const options = toast => ({
  global: {
    mocks: {
      $router: { replace: jest.fn() },
      $store: {
        ui: {
          toast,
        },
      },
    },
  },
})

test('Registration Invalid', () => {
  const toast = jest.fn()
  shallowMount(RegistrationInvalid, options(toast))

  expect(toast).toHaveBeenCalled()
  expect(toast.mock.calls[0][0].level).toBe('danger')
})

test('Registration Complete', () => {
  const toast = jest.fn()
  shallowMount(RegistrationComplete, options(toast))

  expect(toast).toHaveBeenCalled()
  expect(toast.mock.calls[0][0].level).toBe('success')
})
