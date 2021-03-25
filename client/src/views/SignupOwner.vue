<template>
  <div>
    <h1>Buisness Account Sign Up</h1>
    <schema-form form_name="owner/signup" :state="state" :success="success" />
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
    return { state: {} }
  },
  methods: {
    success() {
      this.$router.replace('/signup/complete/')
    },
  },
}
</script>
