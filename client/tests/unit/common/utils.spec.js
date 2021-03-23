import { getCSRF, handleAPIError, slugify } from '@/common/utils'

test('getCSRF', () => {
  expect(getCSRF()).toBe('')
  expect(getCSRF('')).toBe('')
})

test('handleAPIError', () => {
  expect(() => handleAPIError({})).toThrow('')

  const server_error = {
    response: {
      data: {
        errors: { __all__: ['foo'] },
      },
    },
  }
  expect(() => handleAPIError(server_error)).toThrow('')
})

test('slugify', () => {
  expect(slugify('This$$isA   slug-=++')).toBe('this-isa-slug-')
})
