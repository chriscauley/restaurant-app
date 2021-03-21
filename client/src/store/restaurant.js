import Api from './Api'
import slugify from '@/common/slugify'

const DEFAULT_IMG = '/static/pizza.png'

const api = Api()

const prepRestaurant = data => {
  data.img_style = `background-image: url(${data.photo_url || DEFAULT_IMG})`
  data.to = `/restaurant/${data.id}/${slugify(data.name)}/`
  return data
}

const fetchList = (page = 1) => {
  const data = api.get(`restaurants/?page=${page}`)
  data?.items.forEach(prepRestaurant)
  return data
}

const fetchOne = id => {
  const item = api.get(`restaurant/${id}/`)
  return item && prepRestaurant(item)
}

export default { fetchList, fetchOne, markStale: api.markStale }
