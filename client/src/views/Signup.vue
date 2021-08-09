<template>
  <div class="signup-view">
    <h1>Sign Up</h1>
    <schema-form form_name="signup" :state="state" :success="success" />
    <social-links verb="Sign Up" />
    <div class="bottom">
      <router-link class="btn -link" to="/signup/owner/">Register as a business</router-link>
    </div>
  </div>
</template>

<script>
import SocialLinks from '@/components/SocialLinks'

export default {
  components: { SocialLinks },
  __route: {
    path: '/signup/',
    meta: { authRedirect: true },
  },
  data() {
    return { state: {} }
  },
  methods: {
    success() {
      this.$story.complete('auth.signUp.customer')
      this.$router.replace('/signup/complete/')
    },
  },
}
</script>
