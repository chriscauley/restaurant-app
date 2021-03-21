<template>
  <div class="home">
    <h1>Restaurants</h1>
    <div class="restaurant-list row">
      <div v-for="restaurant in restaurants" :key="restaurant.id" class="col-4">
        <router-link class="card" :to="restaurant.to">
          <div class="card__img" :style="restaurant.img_style" />
          <div>{{ restaurant.name }}</div>
        </router-link>
      </div>
    </div>
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
export default {
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
      return this.$store.auth.state.user?.role === 'owner'
    },
  },
  methods: {
    success(data) {
      this.$router.push(`/restaurant/${data.id}/${data.name}/`)
    },
  },
}
</script>
