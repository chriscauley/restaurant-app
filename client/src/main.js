import { createApp } from 'vue'
import App from './App.vue'
import Modal from '@/components/Modal'
import Popper from '@/components/Popper'
import SchemaForm from '@/components/SchemaForm'
import store from '@/store'
import router from '@/router'
import UrForm from '@unrest/vue-form'
import '@/styles/base.scss'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(UrForm.plugin)
app.component('modal', Modal)
app.component('popper', Popper)
app.component('schema-form', SchemaForm)
app.mount('#app')
