import Api from './Api'
import querystring from 'querystring'

const api = Api()

const fetchList = (params = { page: 1 }) => {
  const query = querystring.stringify(params)
  return api.get('orders/?' + query)
}

const fetchOne = id => api.get(`order/${id}/`)

const updateStatus = (id, status) => api.post(`order/${id}/`, { status })
const blockUser = id => api.post(`order/${id}/`, { action: 'block' })
const unblockUser = id => api.post(`order/${id}/`, { action: 'unblock' })

export default {
  fetchList,
  fetchOne,
  updateStatus,
  markStale: api.markStale,
  blockUser,
  unblockUser,
}
