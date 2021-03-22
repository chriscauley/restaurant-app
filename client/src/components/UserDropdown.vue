<template>
  <div class="user-dropdown" v-if="user">
    <div @click="toggleFocus" class="user-dropdown__name">
      <div v-if="user.avatar_url" class="avatar">
        <img :src="user.avatar_url" />
      </div>
      <i class="fa fa-user" v-else />
      {{ user.username }}
      <span v-if="pending_orders" class="notify-dot -red" />
    </div>
    <popper v-if="focused" class="menu" placement="bottom-end">
      <div>
        <router-link to="/order-list/" class="menu-item">
          Orders
          <span v-if="pending_orders" class="badge -red">{{ pending_orders }}</span>
        </router-link>
        <router-link to="/settings" class="menu-item">Settings</router-link>
        <div class="menu-item" @click="logout">Logout</div>
      </div>
    </popper>
  </div>
  <div class="auth-links" v-else>
    <router-link to="/login">Login</router-link>
    <router-link to="/signup">Sign Up</router-link>
  </div>
</template>

<script>
import FocusMixin from './FocusMixin'

export default {
  mixins: [FocusMixin],
  computed: {
    user() {
      return this.$store.auth.state.user
    },
    pending_orders() {
      const orders = this.$store.order.fetchList()?.items || []
      return orders.filter(o => o.allowed_status).length
    },
  },
  methods: {
    logout() {
      this.$store.auth.logout().then(() => {
        this.$store.ui.toast({
          text: 'You have been logged out.',
          level: 'success',
        })
        this.$router.replace('/login')
      })
    },
  },
}
</script>
