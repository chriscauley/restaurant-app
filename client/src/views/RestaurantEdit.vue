<template>
  <div>Restaurant Edit</div>
</template>

<script>
export default {
  __route: {
    path: '/restaurant/edit/:id/:slug/',
    meta: { authRequired: true, requiredRole: 'owner' },
  },
}
</script>
