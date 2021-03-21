import { reactive } from 'vue'

import api from '@/common/api'

export default () => {
  let stale_at = new Date().valueOf()
  const url_fetched_at = {}
  const loading = reactive({})
  const state = reactive({})
  const get = url => {
    const needs_fetch = stale_at > url_fetched_at[url] || !state[url]
    if (needs_fetch && !loading[url]) {
      loading[url] = true
      api.get(url).then(data => {
        url_fetched_at[url] = new Date().valueOf()
        state[url] = data
        loading[url] = false
      })
    }
    return state[url]
  }

  const markStale = () => {
    stale_at = new Date().valueOf()
  }

  const post = (url, data) => {
    api.post(url, data).then(() => {
      markStale()
      get(url)
    })
  }

  return { get, markStale, post }
}
