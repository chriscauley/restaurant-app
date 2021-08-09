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
    <popper v-if="focused" class="menu" placement="bottom-end" offset="16,7">
      <div>
        <router-link to="/orders/" class="menu-item">
          Orders
          <span v-if="pending_orders" class="badge -red">{{ pending_orders }}</span>
        </router-link>
        <router-link to="/settings/" class="menu-item">Settings</router-link>
        <div class="menu-item" @click="logout">Logout</div>
      </div>
    </popper>
  </div>
  <div class="auth-links" v-else>
    <router-link class="btn -link" to="/login">Login</router-link>
    <router-link class="btn -link" to="/signup">Sign Up</router-link>
  </div>
</template>

<script>
import FocusMixin from '@/mixins/FocusMixin'

const getStoryAction = avatar_url => {
  if (avatar_url?.includes('avatars.githubusercontent.com')) {
    return 'auth.social.github'
  } else if (avatar_url?.includes('pbs.twimg.com')) {
    return 'auth.social.twitter'
  }
  return
}

export default {
  mixins: [FocusMixin],
  computed: {
    user() {
      const user = this.$store.auth.get()
      const action = getStoryAction(user?.avatar_url)
      action && this.$story.once(action, user.avatar_url)
      return user
    },
    pending_orders() {
      const orders = this.$store.order.getPage({ page: 1 })?.items || []
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
