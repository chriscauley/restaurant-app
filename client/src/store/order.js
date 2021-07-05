import { RestStorage } from '@unrest/vue-storage'

import client from '@/common/api'

const store = RestStorage('order', { client })

const refetch = ({ id }) => store.getOne(id)

const updateStatus = (id, status) => store.save({ id, status }).then(refetch)
const blockUser = id => store.save({ id, action: 'block' }).then(refetch)
const unblockUser = id => store.save({ id, action: 'unblock' }).then(refetch)

Object.assign(store, { updateStatus, blockUser, unblockUser })

export default store
