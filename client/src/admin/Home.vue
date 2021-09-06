<template>
  <div>
    <div v-for="app in apps" :key="app.app_label">
      <div>
        <h2>
          <router-link :to="`/admin/${app.app_label}/`">{{ app.verbose }}</router-link>
        </h2>
        <ul>
          <li v-for="model in app.models" :key="model.key">
            <router-link :to="`/admin/${app.app_label}/${model.model_name}/`">
              {{ model.verbose }} ({{ model.count }})
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import AppBox from './AppBox'
import store from './store'

export default {
  __route: {
    path: '/admin/',
  },
  components: { AppBox },
  computed: {
    apps() {
      return store.listApps()
    }
  }
}
</script>