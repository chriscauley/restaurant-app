export const RegistrationInvalid = {
  render: () => '',
  __route: {
    path: '/registration/invalid',
    meta: { authRedirect: true },
  },
  mounted() {
    this.$store.ui.toast({
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
    meta: { authRedirect: true },
  },
  mounted() {
    this.$store.ui.toast({
      text: 'Your account has been activated and you are now logged in.',
      level: 'success',
    })
    this.$router.replace('/')
  },
}
