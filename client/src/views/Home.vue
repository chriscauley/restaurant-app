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
  </div>
</template>

<script>
export default {
  __route: {
    path: '/',
    meta: { authRequired: true },
  },
  computed: {
    restaurants() {
      return this.$store.restaurant.fetchList()?.items
    },
  },
}
</script>
