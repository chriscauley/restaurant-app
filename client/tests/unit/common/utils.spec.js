import { getCSRF, handleError, slugify } from '@/common/utils'

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

test('slugify', () => {
  expect(slugify('This$$isA   slug-=++')).toBe('this-isa-slug-')
})
