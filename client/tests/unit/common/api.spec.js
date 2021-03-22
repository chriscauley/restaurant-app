import { getCSRF, handleError } from '@/common/api'

test('getCSRF', () => {
  expect(getCSRF()).toBe('')
  expect(getCSRF('')).toBe('')
})

test('handleError', () => {
  expect(() => handleError({})).toThrow('')

  const server_error = {
    response: {
      data: {
        errors: { __all__: ['foo'] },
      },
    },
  }
  expect(() => handleError(server_error)).toThrow('')
})
