import axios from 'axios'

export const getCSRF = cookie => {
  cookie = cookie || document.cookie
  return cookie.match(/csrftoken=([^;]+)/)?.[1]
}

function handleError(error) {
  error.server_errors = {}
  Object.entries(error.response.data.errors).forEach(([key, errors]) => {
    error.server_errors[key] = errors.map(e => e.message).join(' ')
  })
  throw error
}

const api = axios.create({
  baseURL: '/api',
  transformRequest(data, headers) {
    headers.post['X-CSRFToken'] = getCSRF()
    headers.post['Content-Type'] = 'application/json'
    return JSON.stringify(data)
  },
})
api.interceptors.response.use(r => r.data, handleError)

export default api
