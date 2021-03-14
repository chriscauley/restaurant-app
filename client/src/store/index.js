import auth from './auth'
import cart from './cart'
import restaurant from './restaurant'
import schema from './schema'

const store = {
  list: [],
  install: (app, _options) => {
    app.config.globalProperties.$store = store
    store.list.forEach(m => m.init?.())
  },
}

Object.entries({ auth, cart, restaurant, schema }).forEach(([name, module]) => {
  store.list.push(module)
  store[name] = module
})

export default store
