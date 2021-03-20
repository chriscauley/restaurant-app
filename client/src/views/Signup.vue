<template>
  <div>
    <schema-form form_name="SignupForm" :state="state" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/signup',
    meta: { authRedirect: true },
  },
  data() {
    const r = Math.round(1000 * Math.random())
    return {
      state: {
        username: 'cantelope' + r,
        email: `arst${r}@arst.com`,
        password1: 'no hope heerey1',
        password2: 'no hope heerey1',
      },
    }
  },
}
</script>
