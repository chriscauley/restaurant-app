<template>
  <div class="toast-list">
    <div v-for="toast in toasts" :key="toast.id" :class="`toast -${toast.level}`">
      <div class="text">
        {{ toast.text }}
      </div>
    </div>
  </div>
  <div v-if="alert" class="modal">
    <div class="modal__mask" @click="closeAlert" />
    <div class="modal__content">
      <h2 v-if="alert.title" class="modal__title">
        <i :class="`fa fa-${alert.icon}`" v-if="alert.icon" />
        {{ alert.title }}
      </h2>
      <div class="modal__body">
        {{ alert.text }}
      </div>
      <div class="modal__footer">
        <button class="btn -primary" @click="closeAlert">Ok</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    toasts() {
      return this.$store.ui.state.toasts.filter(t => !t.hidden)
    },
    alert() {
      return this.$store.ui.state.alert
    },
  },
  methods: {
    closeAlert() {
      this.$store.ui.closeAlert()
    },
  },
}
</script>
