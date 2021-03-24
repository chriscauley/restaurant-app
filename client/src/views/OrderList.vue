<template>
  <div class="order-list-view">
    <h2>Order List</h2>
    <div>
      <router-link
        :to="`/order/${order.id}/`"
        v-for="order in orders"
        :key="order.id"
        class="order-item"
      >
        <div :class="getStatusClass(order)">{{ order.status }}</div>
        <div class="description">
          <div>{{ getDescription(order) }}</div>
          <div>from {{ order.restaurant_name }}</div>
        </div>
        <div class="total-price">${{ order.total_price }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/order-list',
    meta: { authRequired: true },
  },
  computed: {
    is_owner() {
      return this.$store.auth.get()?.role === 'owner'
    },
    orders() {
      return this.$store.order.fetchList()?.items
    },
  },
  methods: {
    getDescription(order) {
      const { total_items } = order
      const user = this.is_owner ? order.user_name : 'You'
      return `${user} ordered ${total_items} item${total_items === 1 ? '' : 's'}`
    },
    getStatusClass(order) {
      let color = order.allowed_status ? '-primary' : '-secondary'
      if (order.status === 'canceled') {
        color = '-danger'
      }
      return ['btn', color]
    },
  },
}
</script>
