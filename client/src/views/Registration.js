import unrest from '@unrest/vue'

export const RegistrationInvalid = {
  render: () => '',
  __route: {
    path: '/registration/invalid',
    meta: { authRedirect: true },
  },
  mounted() {
    unrest.ui.toast({
      text: 'This registration link is no longer valid. Please try again.',
      level: 'danger',
    })
    this.$router.replace('/')
  },
}

export const RegistrationComplete = {
  render: () => '',
  __route: {
    path: '/registration/complete/',
  },
  mounted() {
    this.$auth.fetch().then(user => {
      if (user) {
        this.$story.complete('auth.verifyEmail')
        this.$story.complete(`auth.signUp.${user.role}`)
        unrest.ui.toast({
          text: 'Your account has been activated and you are now logged in.',
          level: 'success',
        })
      }
      this.$router.replace('/')
    })
  },
}
