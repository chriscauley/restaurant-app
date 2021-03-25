<template>
  <div class="signup-view">
    <h1>Please Verify Your Account</h1>
    <div>
      Your account has been created. Please check your email and verify your account to continue.
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/signup/complete/',
    meta: { authRedirect: true },
  },
}
</script>
