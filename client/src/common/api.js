import axios from 'axios'

export const getCSRF = cookie => {
  cookie = cookie || document.cookie
  return cookie.match(/csrftoken=([^;]+)/)?.[1]
}

function handleError(error) {
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
