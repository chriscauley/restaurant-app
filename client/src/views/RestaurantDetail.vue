<template>
  <div v-if="restaurant" class="restaurant-detail">
    <h1>{{ restaurant.name }}</h1>
    <div class="row">
      <div class="menu col-8">
        <div v-for="section in restaurant.menusections" :key="section.id" class="menu-section">
          <h2>{{ section.name }}</h2>
          <div class="menu-items row">
            <div v-for="item in section.items" :key="item.id" class="col-6">
              <div class="menu-item" @click="addToCart(item)">
                <div class="menu-item__top">
                  <div class="menu-item__name">{{ item.name }}</div>
                  <div class="menu-item__price">${{ item.price }}</div>
                </div>
                <div class="menu-item__description">{{ item.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-4">
        <h2>Cart</h2>
        <div class="cart">
          <div v-for="item in cart.items" :key="item.id">
            {{ item.name }}
            x{{ item.quantity }}
            {{ item.price }}
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
    cart() {
      return this.$store.cart.state
    },
  },
  methods: {
    addToCart(item) {
      this.$store.cart.addItem(item)
    },
    removeToCart(item) {
      this.$store.cart.removeItem(item)
    },
  },
}
</script>
