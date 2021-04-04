<template>
  <div class="order-detail-view">
    <div v-if="order">
      <h2>Order #{{ order.id }}</h2>
      <div class="row">
        <div class="col-6 left-details">
          <div v-if="photo_url" class="avatar" :style="`background-image: url(${photo_url})`" />
          <div class="user" v-if="order.is_owner">Username: {{ order.user_name }}</div>
          <div class="date">Date: {{ date }}</div>
          <div class="restaurant">Restaurant: {{ order.restaurant_name }}</div>
        </div>
        <div class="col-6">
          <cart v-if="order.items" :items="order.items" />
        </div>
      </div>
      <div v-if="order.status === 'canceled'">
        The order was canceled by the customer.
      </div>
      <div class="progress-bar">
        <div class="rail" />
        <div class="so-far" :style="progress_style" />
        <div class="status-icon" v-for="update in history" :key="update.status">
          <div class="status-content">
            {{ update.status }}
            <div>
              {{ update.date }}
            </div>
          </div>
        </div>
      </div>
      <div class="actions">
        <button v-if="can_cancel" class="btn -danger" @click="cancelling = true">
          Cancel Order
        </button>
        <button v-else-if="order.allowed_status" class="btn -primary" @click="markAllowedStatus">
          Mark order as {{ order.allowed_status }}
        </button>
        <div v-if="order.is_owner" class="block-zone">
          <button v-if="order.is_blocked" @click="unblockUser" class="btn -danger">
            Unblock User
          </button>
          <button v-else @click="blockUser" class="btn -danger">Block User</button>
        </div>
      </div>
      <div v-if="order.is_owner && pages[0]?.items">
        <h2>Past Orders from {{ order.user_name }}</h2>
        <template v-for="(page, index) in pages" :key="index">
          <order-list :orders="page?.items" />
        </template>
        <button v-if="has_next_page" class="btn -primary list-paginator" @click="loadNextPage">
          Load More Orders
        </button>
      </div>
    </div>
    <modal v-if="cancelling" title="Cancel Order" :close="() => (cancelling = false)">
      Are you sure you want to cancel this order? This cannot be undone.
      <template #actions>
        <button class="btn -secondary" @click="cancelling = false">No</button>
        <button class="btn -danger" @click="confirmCancel">Yes, cancel the order</button>
      </template>
    </modal>
  </div>
</template>

<script>
import { formatDistanceToNow, format } from 'date-fns'

import PaginatedMixin from '@/mixins/PaginatedMixin'
import OrderList from '@/components/OrderList'
import Cart from '@/components/Cart'

export default {
  mixins: [PaginatedMixin],
  components: { Cart, OrderList },
  props: {
    POLL_FREQUENCY: {
      type: Number,
      default: () => 15, // seconds to update order
    },
  },
  __route: {
    path: '/order/:order_id/',
    meta: { authRequired: true },
  },
  data() {
    return { cancelling: false }
  },
  mounted() {
    this.timeout = setTimeout(this.poll, this.POLL_FREQUENCY * 1000)
  },
  unmounted() {
    clearTimeout(this.timeout)
  },
  computed: {
    order() {
      return this.$store.order.getOne(this.$route.params.order_id)
    },
    can_cancel() {
      return this.order.allowed_status === 'canceled'
    },
    history() {
      const unslugify = status => {
        status = status.replace(/_/g, ' ')
        return status.slice(0, 1).toUpperCase() + status.slice(1)
      }
      if (!this.order.status_history) {
        return []
      }
      return this.order.status_history.map(({ status, created }) => ({
        status: unslugify(status),
        date: created && format(new Date(created), 'h:mm aaaa'),
      }))
    },
    date() {
      return format(new Date(this.order.created), 'MMM d, yyyy')
    },
    progress_style() {
      const steps = this.history.length - 1
      const steps_done = this.history.filter(h => h.date).length - 1
      return `width: ${(100 * steps_done) / steps}%`
    },
    photo_url() {
      if (this.order.is_owner) {
        return this.order.user_avatar_url
      }
      return this.order.restaurant_photo_url
    },
  },
  methods: {
    poll() {
      clearTimeout(this.timeout)
      this.$store.order.api.markStale()
      this.$store.order.getOne(this.$route.params.order_id)
      if (!['canceled', 'received'].includes(this.order?.status)) {
        this.timeout = setTimeout(this.poll, this.POLL_FREQUENCY * 1000)
      }
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
