import store from '@/store'

const forms = ['login', 'signup', 'restaurant', 'owner/signup', 'menuitem', 'menusection']

forms.forEach(form_name =>
  test('getting schema form ' + form_name, done => {
    store.schema.fetch(form_name)
    setTimeout(() => {
      expect(store.schema.fetch('form_name')).toMatchSnapshot()
      done()
    }, 1000)
  }),
)
