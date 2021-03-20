<template>
  <div>
    <h1>Sign Up</h1>
    <schema-form form_name="SignupForm" :state="state" :success="success" />
    <router-link to="/signup/owner/">Register as a business</router-link>
    <social-links verb="Sign Up" />
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
    // TODO remove dummy state
    const DEBUG = true
    const r = Math.round(1000 * Math.random())
    const dummy_state = {
      username: 'cantelope' + r,
      email: `arst${r}@arst.com`,
      password1: 'no hope heerey1',
    }
    return {
      state: DEBUG ? dummy_state : {},
    }
  },
  methods: {
    success() {
      this.$router.replace('/signup/complete/')
    },
  },
}
</script>
