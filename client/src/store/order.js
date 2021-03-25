import Api from './Api'
import querystring from 'querystring'

const api = Api()

const fetchList = (params = { page: 1 }) => {
  const query = querystring.stringify(params)
  return api.get('orders/?' + query)
}

const fetchOne = id => api.get(`order/${id}/`)

const refetch = ({ id }) => {
  api.markStale()
  fetchOne(id)
}

const updateStatus = (id, status) => api.post(`order/${id}/`, { status }).then(refetch)
const blockUser = id => api.post(`order/${id}/`, { action: 'block' }).then(refetch)
const unblockUser = id => api.post(`order/${id}/`, { action: 'unblock' }).then(refetch)

export default {
  fetchList,
  fetchOne,
  updateStatus,
  markStale: api.markStale,
  blockUser,
  unblockUser,
}
