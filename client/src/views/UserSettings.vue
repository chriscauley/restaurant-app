<template>
  <div>
    <schema-form form_name="UserSettingsForm/self" :success="success" :prepSchema="prepSchema" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/settings/',
    meta: { authRequired: true },
  },
  methods: {
    prepSchema(schema) {
      schema.properties.avatar_url.type = 'image'
      schema.properties.avatar_url.title = 'Avatar'
      return schema
    },
    success() {
      this.$store.ui.toast({
        text: 'Settings updated',
      })
    },
  },
}
</script>
