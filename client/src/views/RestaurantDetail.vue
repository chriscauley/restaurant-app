<template>
  <div v-if="restaurant" class="restaurant-detail">
    <h1>{{ restaurant.name }}</h1>
    <div class="menu">
      <div v-for="section in restaurant.menusections" :key="section.id" class="menu-section">
        <h2>{{ section.name }}</h2>
        <div class="menu-items row">
          <div v-for="item in section.items" :key="item.id" class="col-6">
            <div class="menu-item">
              <div class="menu-item__name">{{ item.name }}</div>
              <div class="menu-item__price">${{ item.price }}</div>
              <div class="menu-item__description">{{ item.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/restaurant/:id/:slug/',
  },
  computed: {
    restaurant() {
      return this.$store.restaurant.fetchmenu(this.$route.params.id)
    },
  },
}
</script>
