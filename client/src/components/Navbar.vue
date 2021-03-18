<template>
  <header class="navbar">
    <router-link to="/" class="navbar__brand">
      <img src="/static/pizza.png" />
      Top Table
    </router-link>
    <user-dropdown />
  </header>
</template>

<script>
import UserDropdown from './UserDropdown'
export default {
  components: { UserDropdown },
}
</script>
