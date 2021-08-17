<template>
  <div v-if="restaurant" class="restaurant-view">
    <h1>
      {{ restaurant.name }}
      <i class="fa fa-edit" v-if="is_owner" @click="edit('restaurant', restaurant.id)" />
    </h1>
    <h3>{{ restaurant.description }}</h3>
    <p v-if="!is_owner">
      Click any meal to add it to your cart.
    </p>
    <div class="row">
      <div class="menu col-8">
        <div v-for="section in restaurant.menusections" :key="section.id" class="menu-section">
          <div class="menu-title">
            <h2>
              <i class="fa fa-edit" v-if="is_owner" @click="edit('menusection', section.id)" />
              {{ section.name }}
            </h2>
            <div v-if="is_owner">
              <button class="btn -primary" @click="addMenuItem(section)">
                Add menu item
              </button>
            </div>
          </div>
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
          </div>
        </div>
        <div v-if="is_owner">
          <div class="hr" />
          <button class="btn -primary" @click="addMenuSection">
            Add another menu section
          </button>
        </div>
      </div>
      <div class="col-4">
        <div v-if="cart" class="cart-box">
          <h2>Cart</h2>
          <div v-if="show_warning" class="alert -warning">
            You already have a cart open with another restaurant. Adding items on this page will
            clear your existing cart.
          </div>
          <cart
            v-else-if="cart.items"
            :addItem="addItem"
            :removeItem="removeItem"
            :checkout="checkout"
            :items="cart.items"
          />
        </div>
      </div>
    </div>
    <unrest-modal v-if="form_attrs" @close="form_name = null">
      <unrest-schema-form v-bind="form_attrs" />
      <template #actions>{{ ' ' }}</template>
    </unrest-modal>
  </div>
</template>

<script>
import Cart from '@/components/Cart'

export default {
  components: { Cart },
  __route: {
    path: '/restaurant/:id/:slug/',
    meta: { authRequired: true },
  },
  data() {
    if (this.$auth.get().role === 'user') {
      this.$story.complete('customer.restaurantDetail')
    }
    return { form_name: null, form_state: null }
  },
  computed: {
    story_action() {
      const [_schema, model_slug, id] = this.form_name.split('/')
      const verb = id ? 'update' : 'create'
      const from_slug = {
        restaurant: 'Restaurant',
        menuitem: 'MenuItem',
        menusection: 'MenuSection',
      }
      return `owner.${from_slug[model_slug]}.${verb}`
    },
    restaurant() {
      return this.$store.restaurant.getOne(this.$route.params.id)
    },
    cart() {
      return !this.is_owner && this.$store.cart.get()
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
      const exists = !!this.form_name.match(/\/\d+/)
      return {
        onDelete: exists ? this.onDelete : undefined,
        form_name: this.form_name,
        state: this.form_state || {},
        success: data => {
          this.$story.complete(this.story_action)
          this.form_name = this.form_state = null
          this.$store.restaurant.api.markStale()
          this.$store.restaurant.getOne(this.$route.params.id)
          this.$ui.toast({
            text: `Updated "${data.name}"`,
            level: 'success',
          })
        },
      }
    },
    show_warning() {
      return this.cart.restaurant_id && this.cart.restaurant_id !== this.restaurant.id
    },
  },
  methods: {
    addItem(item_id) {
      if (!this.is_owner) {
        this.$story.complete('customer.updateCartItem')
        this.$store.cart.addItem(item_id)
      }
    },
    removeItem(item_id) {
      if (!this.is_owner) {
        this.$story.complete('customer.updateCartItem')
        this.$store.cart.removeItem(item_id)
      }
    },
    checkout() {
      this.$store.cart.checkout()
    },
    addMenuSection() {
      this.form_name = 'schema/menusection'
      this.form_state = {
        restaurant: this.$route.params.id,
      }
    },
    addMenuItem(section) {
      this.form_name = 'schema/menuitem'
      this.form_state = {
        menusection: section.id,
      }
    },
    edit(model, id) {
      this.form_name = `schema/${model}/${id}`
    },
    onDelete(name) {
      this.$story.complete(this.story_action.replace(/(create|update)/, 'delete'))
      if (this.form_name.includes('restaurant')) {
        this.$router.replace('/')
      } else {
        this.$store.restaurant.api.markStale()
        this.$store.restaurant.getOne(this.$route.params.id)
        this.form_name = null
      }
      this.$ui.toast({
        text: `"${name}" has been deleted.`,
        level: 'success',
      })
    },
  },
}
</script>
