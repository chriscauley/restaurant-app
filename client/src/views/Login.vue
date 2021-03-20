<template>
  <div>
    <schema-form form_name="LoginForm" :success="success" />
    <social-links verb="Login" />
  </div>
</template>

<script>
import SocialLinks from '@/components/SocialLinks'
export default {
  components: { SocialLinks },
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
