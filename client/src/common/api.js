import axios from 'axios'

export const getCSRF = (cookie = '') => {
  return cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
}

export function handleError(error) {
  error.server_errors = {}
  Object.entries(error.response?.data.errors || {}).forEach(([key, errors]) => {
    error.server_errors[key] = errors.map(e => e.message).join(' ')
  })
  throw error
}

const root = process.env.VUE_APP_ROOT_URL || ''

const api = axios.create({
  baseURL: root + '/api',
  transformRequest(data, headers) {
    headers.post['X-CSRFToken'] = getCSRF(document.cookie)
    headers.post['Content-Type'] = 'application/json'
    return JSON.stringify(data)
  },
})
api.interceptors.response.use(r => r.data, handleError)

export default api
