<template>
  <ul class="restaurant-list">
    <li v-for="restaurant in $store.restaurant.all()" :key="restaurant.id">
      {{ restaurant.name }}
    </li>
  </ul>
</template>

<script>
export default {};
</script>
