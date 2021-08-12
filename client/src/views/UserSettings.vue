<template>
  <div class="user-settings-view">
    <unrest-schema-form
      :form_name="`schema/UserSettingsForm/${$auth.user.id}`"
      :success="success"
    />
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
      this.$ui.toast({
        text: 'Settings updated',
        level: 'success',
      })
    },
  },
}
</script>
