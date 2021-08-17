import { range } from 'lodash'
export const self_user = {
  user: { id: 2, email: '', username: 'user', role: 'user', avatar_url: null },
}

export const getRestaurantPage = (opts = {}) => {
  const { pages = 1, page = 1, per_page = 12, count = per_page } = opts
  const MIN_ID = (page - 1) * per_page + 1
  return {
    pages,
    items: range(count).map((i) => {
      const id = i + MIN_ID
      return {
        name: `Restaurant #${id}`,
        photo_url: '/media/photo.png',
        // description
      }
    }),
  }
}
