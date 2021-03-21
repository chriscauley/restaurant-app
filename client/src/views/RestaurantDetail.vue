<template>
  <div v-if="restaurant" class="restaurant-detail">
    <h1>{{ restaurant.name }}</h1>
    <div class="row">
      <div class="menu col-8">
        <div v-for="section in restaurant.menusections" :key="section.id" class="menu-section">
          <h2>{{ section.name }}</h2>
          <div class="menu-items row">
            <div v-for="item in section.items" :key="item.id" class="col-6">
              <div class="menu-item" @click="addItem(item.id)">
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
          <div v-for="item in cart.items" :key="item.id" class="cart-item">
            <div class="cart-item__top">
              <div class="cart-item__name">{{ item.name }}</div>
              <div class="cart-item__total">${{ item.price * item.quantity }}</div>
            </div>
            <div class="cart-item__bottom">
              ${{ item.price }} x {{ item.quantity }}
              <div class="action" @click="removeItem(item.menuitem_id)">-</div>
              <div class="action" @click="addItem(item.menuitem_id)">+</div>
            </div>
          </div>
          <div class="cart-total">${{ total }}</div>
          <button class="btn btn-primary" @click="checkout">
            Checkout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/restaurant/:id/:slug/',
    meta: { authRequired: true },
  },
  computed: {
    restaurant() {
      return this.$store.restaurant.fetchOne(this.$route.params.id)
    },
    cart() {
      return this.$store.cart.state
    },
    total() {
      let total = 0
      this.cart.items.forEach(item => (total += item.price * item.quantity))
      return total
    },
  },
  methods: {
    addItem(item_id) {
      this.$store.cart.addItem(item_id)
    },
    removeItem(item_id) {
      this.$store.cart.removeItem(item_id)
    },
    checkout() {
      this.$store.cart.checkout()
    },
  },
}
</script>
