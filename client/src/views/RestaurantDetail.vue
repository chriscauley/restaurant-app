<template>
  <div v-if="restaurant" class="restaurant-detail">
    <h1>
      {{ restaurant.name }}
      <i class="fa fa-edit" v-if="is_owner" @click="edit('restaurant', restaurant.id)" />
    </h1>
    <h3>{{ restaurant.description }}</h3>
    <div class="row">
      <div class="menu col-8">
        <div v-for="section in restaurant.menusections" :key="section.id" class="menu-section">
          <h2>
            {{ section.name }}
            <i class="fa fa-edit" v-if="is_owner" @click="edit('menusection', section.id)" />
          </h2>
          <div class="menu-items row">
            <div v-for="item in section.items" :key="item.id" class="col-6">
              <div class="menu-item" @click="addItem(item.id)">
                <div class="menu-item__top">
                  <div class="menu-item__name">
                    <i class="fa fa-edit" v-if="is_owner" @click="edit('menuitem', item.id)" />
                    {{ item.name }}
                  </div>
                  <div class="menu-item__price">${{ item.price }}</div>
                </div>
                <div class="menu-item__description">{{ item.description }}</div>
              </div>
            </div>
            <div class="col-6 flex-grow" v-if="is_owner">
              <button class="btn -primary" @click="addMenuItem(section)">
                Add another item
              </button>
            </div>
          </div>
        </div>
        <div v-if="is_owner">
          <div class="hr" />
          <div class="hr" />
          <button class="btn -primary" @click="addMenuSection">
            Add another menu section
          </button>
        </div>
      </div>
      <div v-if="!is_owner" class="col-4">
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
    <modal v-if="form_name" :close="() => (form_name = null)">
      <schema-form v-bind="form_attrs" />
      <template #actions>{{ ' ' }}</template>
    </modal>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/restaurant/:id/:slug/',
    meta: { authRequired: true },
  },
  data() {
    return { form_name: null, form_state: null }
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
    is_owner() {
      return this.restaurant.is_owner
    },
    form_attrs() {
      if (!this.form_name) {
        return
      }
      return {
        form_name: this.form_name,
        state: this.form_state || {},
        success: data => {
          this.form_name = this.form_state = null
          this.$store.restaurant.markStale()
          this.$store.restaurant.fetchOne(this.$route.params.id)
          this.$store.ui.toast({
            text: `Updated "${data.name}"`,
            level: 'success',
          })
        },
      }
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
    addMenuSection() {
      this.form_name = 'menusection'
      this.form_state = {
        restaurant: this.$route.params.id,
      }
    },
    addMenuItem(section) {
      this.form_name = 'menuitem'
      this.form_state = {
        menusection: section.id,
      }
    },
    edit(model, id) {
      this.form_name = `${model}/${id}`
    },
  },
}
</script>
