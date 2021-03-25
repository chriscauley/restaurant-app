<template>
  <div class="cart">
    <div v-if="items.length === 0">
      Your cart is empty
    </div>
    <div v-for="item in items" :key="item.id" class="cart-item">
      <div class="cart-item__top">
        <div class="cart-item__name">{{ item.name }}</div>
        <div class="price">${{ (item.price * item.quantity).toFixed(2) }}</div>
      </div>
      <div class="cart-item__bottom">
        ${{ item.price }} x {{ item.quantity }}
        <template v-if="addItem">
          <div class="action" @click="removeItem(item.menuitem_id)">-</div>
          <div class="action" @click="addItem(item.menuitem_id)">+</div>
        </template>
      </div>
    </div>
    <div class="cart__bottom" v-if="items.length">
      <button class="btn -primary" @click="checkout" v-if="checkout">
        Checkout
      </button>
      <div class="cart__total">
        Total:
        <span class="price">${{ total.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: Array,
    addItem: Function,
    removeItem: Function,
    checkout: Function,
  },
  computed: {
    total() {
      let total = 0
      this.items.forEach(item => (total += item.price * item.quantity))
      return total
    },
  },
}
</script>
