<template>
  <div class="home-view">
    <h1>Restaurants</h1>
    <restaurant-list v-if="restaurants" :restaurants="restaurants" />
    <div v-if="is_owner">
      <button class="btn -primary" @click="adding = true">
        Add another restaurant
      </button>
    </div>
    <modal v-if="adding">
      <schema-form form_name="restaurant" :success="success" />
      <template #actions>{{ ' ' }}</template>
    </modal>
  </div>
</template>

<script>
import RestaurantList from '@/components/RestaurantList'

export default {
  components: { RestaurantList },
  __route: {
    path: '/',
    meta: { authRequired: true },
  },
  data() {
    return { adding: false }
  },
  computed: {
    restaurants() {
      return this.$store.restaurant.fetchList()?.items
    },
    is_owner() {
      return this.$store.auth.get()?.role === 'owner'
    },
  },
  methods: {
    success(data) {
      this.$router.push(`/restaurant/${data.id}/${data.name}/`)
    },
  },
}
</script>
