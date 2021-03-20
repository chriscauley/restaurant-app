<template>
  <div>
    <h1>Buisness Account Sign Up</h1>
    <schema-form form_name="OwnerSignupForm" :state="state" :success="success" />
    <router-link to="/signup/">Not a business? Register as a customer</router-link>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/signup/owner/',
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
