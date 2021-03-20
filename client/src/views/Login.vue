<template>
  <div>
    <schema-form form_name="LoginForm" />
  </div>
</template>

<script>
export default {
  __route: {
    path: '/login',
    meta: { authRedirect: true },
  },
}
</script>
