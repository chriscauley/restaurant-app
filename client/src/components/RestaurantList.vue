<template>
  <div class="restaurant-list row">
    <div v-for="restaurant in restaurants" :key="restaurant.id" class="col-4">
      <router-link class="card" :to="restaurant.to">
        <div class="card__img" :style="restaurant.img_style" />
        <div class="card__title">{{ restaurant.name }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    restaurants: Array,
  },
}
</script>
