<template>
  <div class="orders-view">
    <h2>Order List</h2>
    <order-list :orders="orders" />
  </div>
</template>

<script>
import OrderList from '@/components/OrderList'

export default {
  components: { OrderList },
  __route: {
    path: '/orders/',
    meta: { authRequired: true },
  },
  computed: {
    orders() {
      return this.$store.order.fetchList()?.items
    },
  },
}
</script>
