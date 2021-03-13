import { reactive } from 'vue'

import api from '@/common/api'

const state = reactive({})

const fetch = form_name => {
  if (!state[form_name]) {
    api.get(`schema/${form_name}/`).then(r => (state[form_name] = r.schema))
  }
  return state[form_name]
}

export default { fetch }
