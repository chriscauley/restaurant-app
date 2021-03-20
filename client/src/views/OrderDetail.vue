<template>
  <div class="order-detail">
    <div v-if="order">
      <h2>You ordered from {{ order.restaurant_name }} {{ formatDistanceToNow(order.created) }}</h2>
      <div>
        <button v-if="can_cancel" class="btn btn-cancel" @click="cancelling = true">
          Cancel Order
        </button>
      </div>
      <div class="order__items">
        <div v-for="item in order.items" :key="item.id" class="order-item">
          <div class="order-item__name">{{ item.name }}</div>
          <div class="order-item__price">${{ item.price }}</div>
          <div class="order-item__quantity">x{{ item.quantity }}</div>
        </div>
      </div>
      <div class="order-history">
        <div v-for="history in order.status_history" :key="history.id">
          <div class="order-history__status">{{ history.status }}</div>
          <div class="order-history__since">{{ formatDistanceToNow(history.created) }}</div>
        </div>
      </div>
    </div>
    <modal v-if="cancelling" title="Cancel Order" :close="() => (cancelling = false)">
      Are you sure you want to cancel this order? This cannot be undone.
      <template #actions>
        <button class="btn btn-secondary" @click="cancelling = false">No</button>
        <button class="btn btn-danger" @click="confirmCancel">Yes, cancel the order</button>
      </template>
    </modal>
  </div>
</template>

<script>
import { formatDistanceToNow } from 'date-fns'

export default {
  __route: {
    path: '/order/:order_id/',
    meta: { authRequired: true },
  },
  data() {
    return { cancelling: false }
  },
  computed: {
    order() {
      return this.$store.order.fetch(this.$route.params.order_id)
    },
    can_cancel() {
      return this.order.allowed_statuses.includes('canceled')
    },
  },
  methods: {
    formatDistanceToNow(s) {
      return formatDistanceToNow(new Date(s).valueOf()) + ' ago'
    },
    confirmCancel() {
      this.$store.order.cancel(this.order.id)
      this.cancelling = false
    },
  },
}
</script>
