<template>
  <div class="orders-view">
    <h2>Order List</h2>
    <template v-for="(page, index) in pages" :key="index">
      <order-list :orders="page?.items" />
    </template>
    <button v-if="has_next_page" class="btn -primary list-paginator" @click="loadNextPage">
      Load More Orders
    </button>
  </div>
</template>

<script>
import PaginatedMixin from '@/mixins/PaginatedMixin'
import OrderList from '@/components/OrderList'

export default {
  mixins: [PaginatedMixin],
  components: { OrderList },
  __route: {
    path: '/orders/',
    meta: { authRequired: true },
  },
  methods: {
    getPage(page) {
      return this.$store.order.getPage({ page })
    },
  },
}
</script>
