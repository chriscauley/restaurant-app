import { startCase } from 'lodash'
import views from './views'

const admin = {
  list: [],
  views,
  register: (slug, module) => {
    module.slug = slug
    module.name = module.name || startCase(slug)
    admin.list.push(module)
    admin[slug] = module
  },
}

export default admin