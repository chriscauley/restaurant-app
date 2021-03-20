export default {
  render: () => '',
  __route: {
    path: '/registration/complete/',
  },
  mounted() {
    this.$store.ui.toast({
      text: 'Your account has been activated and you are now logged in.',
      level: 'success',
    }),
      this.$router.replace('/')
  },
}
