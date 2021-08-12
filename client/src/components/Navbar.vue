<template>
  <header class="navbar">
    <router-link to="/" class="navbar__brand">
      <img src="/static/pizza.png" />
      Top Table
    </router-link>
    <unrest-auth-menu :items="items" />
  </header>
</template>

<script>
export default {
  data() {
    return { items: [{ to: '/settings/', text: 'Settings' }] }
  },
}
</script>
