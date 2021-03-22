import store from '@/store'

test.skip('store', done => {
  store.schema.fetch('login')
  setTimeout(() => {
    expect(store.schema.fetch('login')).toMatchSnapshot()
    done()
  }, 1000)
})
