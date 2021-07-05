import { RestStorage } from '@unrest/vue-storage'

import client from '@/common/api'

import { slugify } from '@/common/utils'

const DEFAULT_IMG = '/static/pizza.png'

const fromServer = data => {
  data.img_style = `background-image: url(${data.photo_url || DEFAULT_IMG})`
  data.to = `/restaurant/${data.id}/${slugify(data.name)}/`
  return data
}

export default RestStorage('restaurant', { client, fromServer })
