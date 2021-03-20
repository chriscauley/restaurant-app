<template>
  <div class="user-dropdown" v-if="user">
    <div @click="toggleFocus">
      <i class="fa fa-user" />
      {{ user.username }}
    </div>
    <popper v-if="focused" class="menu">
      <div>
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
