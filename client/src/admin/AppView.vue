<template>
  <div>
    <app-box v-if="app" :app="app" />
  </div>
</template>

<script>
import store from './store'
import AppBox from './AppBox.vue'

export default {
  components: { AppBox },
  __route: {
    path: '/admin/:app_label/',
  },
  computed: {
    apps() {
      return store.listApps().find(a => a.app_label === this.$route.params.app_label)
    }
  }
}
</script>