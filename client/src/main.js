import { createApp } from 'vue'
import UrForm from '@unrest/vue-form'
import '@/styles/base.scss'
import uS from '@unrest/story'

import App from '@/App.vue'
import Modal from '@/components/Modal'
import Popper from '@/components/Popper'
import SchemaForm from '@/components/SchemaForm'
import store from '@/store'
import stories from '@/stories.yaml'
import router from '@/router'

const app = createApp(App)
app.use(uS, stories)
app.use(store)
app.use(router)
app.use(UrForm.plugin)
app.component('modal', Modal)
app.component('popper', Popper)
app.component('schema-form', SchemaForm)
app.mount('#app')
