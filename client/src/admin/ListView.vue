<template>
  <div>
    <div v-for="item in items" :key="item.id">{{ item.id }}</div>
  </div>
</template>

<script>
import store from './store'

export default {
  __route: {
    path: '/admin/:app_label/:model_name/'
  },
  computed: {
    model() {
      return store.getModel(this.$route.params)
    },
    items() {
      return this.model?.getPage()?.items || []
    },
  }
}
</script>