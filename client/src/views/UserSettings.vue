<template>
  <div class="user-settings-view">
    <schema-form form_name="settings/self" :success="success" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/settings/',
    meta: { authRequired: true },
  },
  methods: {
    success(data) {
      this.$story.once('settings.updateAvatar', data.avatar_url)
      this.$story.once('settings.updateUsername', data.username)
      this.$store.ui.toast({
        text: 'Settings updated',
        level: 'success',
      })
    },
  },
}
</script>
