import { reactive } from 'vue'

import api from '@/common/api'

const state = reactive({})

const fetch = form_name => {
  if (!state[form_name]) {
    api.get(`${form_name}/?schema=1`).then(r => (state[form_name] = r.schema))
  }
  return state[form_name]
}

const markStale = form_name => delete state[form_name]

export default { fetch, markStale }
