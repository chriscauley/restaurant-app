import axios from 'axios'
import { getCSRF, handleError } from './utils'

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
