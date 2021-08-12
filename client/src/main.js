import { createApp } from 'vue'
import unrest from '@unrest/vue'
import UrForm from '@unrest/vue-form'
import auth from '@unrest/vue-auth'
import uS from '@unrest/story'

import App from '@/App.vue'
import store from '@/store'
import stories from '@/stories.yaml'
import router from '@/router'
import '@/styles/base.scss'

auth.configure({
  AUTH_START: '/',
  oauth_providers: ['twitter', 'github'],
  enabled: !process.env.VUE_APP_OFFLINE,
})

auth.config.modes[0].text = 'Welcome to Top Table. Please login to continue.'
auth.config.modes[1].extra = () => (
  <div class="bottom">
    <router-link class="btn -link" to="/auth/sign-up-owner/">
      Register as a business
    </router-link>
  </div>
)

auth.config.modes.push({
  slug: 'sign-up-owner',
  form_name: 'schema/OwnerSignUpForm',
  title: 'Buisness Sign Up',
  extra: () => (
    <div class="bottom">
      <router-link to="/auth/sign-up/" class="btn -link">
        Not a business? Register as a customer
      </router-link>
    </div>
  ),
})

const app = createApp(App)
app.use(uS, stories)
app.use(store)
app.use(router)
app.use(UrForm.plugin)
app.use(unrest.plugin)
app.use(unrest.ui)
app.use(auth.plugin)

app.mount('#app')
