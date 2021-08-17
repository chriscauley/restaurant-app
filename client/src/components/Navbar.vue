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
  computed: {
    items() {
      const orders = this.$store.order.getPage({ page: 1 })?.items || []
      const pending_orders = orders.filter(o => o.allowed_status).length
      const OrderLink = () => (
        <router-link to="/orders/">
          Orders
          {pending_orders > 0 && <span class="badge -red">{pending_orders}</span>}
        </router-link>
      )

      return [{ to: '/settings/', text: 'Settings' }, { tagName: OrderLink }]
    },
  },
}
</script>
