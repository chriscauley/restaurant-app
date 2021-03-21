<template>
  <div>
    <schema-form form_name="UserSettingsForm/self" :success="success" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/settings/',
    meta: { authRequired: true },
  },
  methods: {
    success() {
      this.$store.ui.toast({
        text: 'Settings updated',
      })
    },
  },
}
</script>
