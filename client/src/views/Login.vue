<template>
  <div>
    <schema-form form_name="LoginForm" :success="success" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/login',
    meta: { authRedirect: true },
  },
  methods: {
    success() {
      this.$store.auth.refetch().then(
        // reload route to cause router to redirect to next or /
        () => this.$router.replace(this.$route.query.next || '/'),
      )
    },
  },
}
</script>
