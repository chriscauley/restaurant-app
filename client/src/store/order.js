import Api from './Api'

const api = Api()

const fetchList = () => api.get('order/')
const fetchOne = id => api.get(`order/${id}/`)

const updateStatus = (id, status) => api.post(`order/${id}/`, { status })

export default { fetchList, fetchOne, updateStatus, markStale: api.markStale }
