<template>
  <div class="home-view">
    <div class="home-view__top">
      <h1>Restaurants</h1>
      <div v-if="is_owner">
        <button class="btn -primary" @click="adding = true">
          Add another restaurant
        </button>
      </div>
    </div>
    <p v-if="!is_owner">
      Click a restaurant to start your order.
    </p>
    <template v-for="(page, index) in pages" :key="index">
      <restaurant-list v-if="page" :restaurants="page.items" />
    </template>
    <button v-if="has_next_page" class="btn -primary list-paginator" @click="loadNextPage">
      Load More Restaurants
    </button>
    <modal v-if="adding">
      <schema-form form_name="restaurant" :success="success" />
      <template #actions>{{ ' ' }}</template>
    </modal>
  </div>
</template>

<script>
import PaginatedMixin from '@/mixins/PaginatedMixin'
import RestaurantList from '@/components/RestaurantList'

export default {
  mixins: [PaginatedMixin],
  components: { RestaurantList },
  __route: {
    path: '/',
    meta: { authRequired: true },
  },
  data() {
    return { adding: false }
  },
  computed: {
    is_owner() {
      return this.$store.auth.get()?.role === 'owner'
    },
  },
  methods: {
    getPage(page) {
      return this.$store.restaurant.fetchList({ page })
    },
    success(data) {
      this.$router.push(`/restaurant/${data.id}/${data.name}/`)
    },
  },
}
</script>
