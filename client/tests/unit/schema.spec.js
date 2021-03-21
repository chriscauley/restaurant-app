import store from '@/store'

test("store", (done) => {
  store.schema.fetch('login')
  setTimeout(() => {
    console.log(store.schema.fetch('login'))
    done()
  }, 1000)
})