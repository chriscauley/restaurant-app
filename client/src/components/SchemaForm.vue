<template>
  <ur-form v-if="schema" :schema="schema" v-bind="$attrs" :onSubmit="submit" :errors="errors" />
</template>

<script>
import api from '@/common/api'

export default {
  props: {
    form_name: String,
    success: Function,
    prepSchema: {
      type: Function,
      default: a => a,
    },
  },
  data() {
    return { errors: null, loading: false }
  },
  computed: {
    schema() {
      const schema = this.$store.schema.fetch(this.form_name)
      return schema ? this.prepSchema(schema) : schema
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
