<template>
  <div class="order-detail">
    <div v-if="order">
      <h2>You ordered from {{ order.restaurant_name }} {{ formatDistanceToNow(order.created) }}</h2>
      <div>
        <button v-if="can_cancel" class="btn btn-cancel" @click="cancelling = true">
          Cancel Order
        </button>
        <button v-else-if="order.allowed_status" class="btn btn-success" @click="markAllowedStatus">
          Mark order as {{ order.allowed_status }}
        </button>
      </div>
      <div class="row">
        <div class="col-6">
          <div class="order__items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <div class="order-item__name">{{ item.name }}</div>
              <div class="order-item__price">${{ item.price }}</div>
              <div class="order-item__quantity">x{{ item.quantity }}</div>
            </div>
          </div>
        </div>
        <div class="order-history col-6">
          <div v-for="update in history" :key="update.status">
            {{ update.status }}
            {{ update.ago }}
          </div>
          <div v-if="order.status === 'canceled'">
            The order was canceled by the customer.
          </div>
        </div>
      </div>
      <div v-if="order.is_owner" class="block-zone">
        <div>
          <button v-if="order.is_blocked" @click="unblockUser" class="btn -danger">
            Unblock User
          </button>
          <button v-else @click="blockUser" class="btn -danger">Block User</button>
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

const POLL_FREQUENCY = 15 // seconds to update order

export default {
  __route: {
    path: '/order/:order_id/',
    meta: { authRequired: true },
  },
  data() {
    return { cancelling: false }
  },
  mounted() {
    this.timeout = setTimeout(this.poll, POLL_FREQUENCY * 1000)
  },
  unmounted() {
    clearTimeout(this.timeout)
  },
  computed: {
    order() {
      return this.$store.order.fetchOne(this.$route.params.order_id)
    },
    can_cancel() {
      return this.order.allowed_status === 'canceled'
    },
    history() {
      const getDate = created => {
        return created && `${formatDistanceToNow(new Date(created))} ago`
      }
      return this.order.status_history.map(({ status, created }) => ({
        status,
        ago: getDate(created),
      }))
    },
  },
  methods: {
    poll() {
      clearTimeout(this.timeout)
      this.$store.order.markStale()
      this.$store.order.fetchOne(this.$route.params.order_id)
      if (!['canceled', 'received'].includes(this.order?.status)) {
        this.timeout = setTimeout(this.poll, POLL_FREQUENCY * 1000)
      }
    },
    getVerboseStatus(status) {
      const title = s => s[0].toUpperCase() + s.slice(1)
      return status.replace('_', ' ').replace(/(\w*\W*|\w*)\s*/g, title)
    },
    formatDistanceToNow(s) {
      return formatDistanceToNow(new Date(s).valueOf()) + ' ago'
    },
    confirmCancel() {
      this.$store.order.updateStatus(this.order.id, 'canceled')
      this.cancelling = false
    },
    markAllowedStatus() {
      const { id, allowed_status } = this.order
      this.$store.order.updateStatus(id, allowed_status)
    },
    blockUser() {
      this.$store.order.blockUser(this.order.id)
    },
    unblockUser() {
      this.$store.order.unblockUser(this.order.id)
    },
  },
}
</script>
