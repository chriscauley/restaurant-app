export const getCSRF = (cookie = '') => {
  return cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
}

export function handleAPIError(error) {
  error.server_errors = {}
  Object.entries(error.response?.data.errors || {}).forEach(([key, errors]) => {
    error.server_errors[key] = errors.map(e => e.message).join(' ')
  })
  throw error
}

export const slugify = s => s.toLowerCase().replace(/\W+/g, '-')
