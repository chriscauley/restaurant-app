<template>
  <div class="login-view">
    <h1>Login</h1>
    <p>
      Welcome to Top Table. Please login to continue.
    </p>
    <schema-form form_name="login" :success="success" />
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
