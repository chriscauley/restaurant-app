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
    <unrest-modal v-if="adding" @close="adding = null">
      <unrest-schema-form form_name="schema/restaurant" :success="success" />
      <template #actions>{{ ' ' }}</template>
    </unrest-modal>
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
      if (this.$auth.get().role === 'user') {
        this.$story.complete('customer.restaurantList')
      }
      return this.$auth.get()?.role === 'owner'
    },
  },
  methods: {
    getPage(page) {
      return this.$store.restaurant.getPage({ page })
    },
    success(data) {
      this.$story.complete('owner.Restaurant.create')
      this.$router.push(`/restaurant/${data.id}/${data.name}/`)
    },
  },
}
</script>
