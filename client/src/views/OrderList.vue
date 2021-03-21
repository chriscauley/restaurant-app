<template>
  <div class="order-list">
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
          {{ getDescription(order) }}
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
      return this.$store.auth.state.user?.role === 'owner'
    },
    orders() {
      return this.$store.order.fetchList()?.items
    },
  },
  methods: {
    getDescription(order) {
      const user_name = this.is_owner ? order.user_name : 'You'
      const { total_items, restaurant_name } = order
      return `${user_name} ordered ${total_items} from ${restaurant_name}.`
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
