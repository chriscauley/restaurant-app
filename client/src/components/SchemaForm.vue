<template>
  <ur-form v-if="schema" :schema="schema" v-bind="$attrs" :onSubmit="submit" :errors="errors" />
</template>

<script>
import api from '@/common/api'

export default {
  props: {
    form_name: String,
    success: Function,
  },
  data() {
    return { errors: null, loading: false }
  },
  computed: {
    schema() {
      return this.$store.schema.fetch(this.form_name)
    },
  },
  methods: {
    submit(state) {
      if (this.loading) {
        return
      }
      this.errors = null
      this.loading = true
      api
        .post(`schema/${this.form_name}/`, state)
        .catch(e => {
          this.errors = e.server_errors || { __all__: 'An unknown error has occurred' }
        })
        .then(result => {
          this.loading = false
          if (!this.errors) {
            this.success?.(result)
          }
        })
    },
  },
}
</script>
