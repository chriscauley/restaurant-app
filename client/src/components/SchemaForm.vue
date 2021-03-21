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
      if (!schema) {
        return
      }
      if (schema.properties.avatar_url) {
        schema.properties.avatar_url.type = 'image'
        schema.properties.avatar_url.title = 'Avatar'
      }
      if (schema.properties.photo_url) {
        schema.properties.photo_url.type = 'image'
        schema.properties.photo_url.title = 'Photo'
      }
      Object.values(schema.properties).forEach(property => {
        if (property.__widget === 'HiddenInput') {
          property.ui = { tagName: 'ur-hidden' }
        }
      })
      return schema
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
            this.$store.schema.markStale(this.form_name)
          }
        })
    },
  },
}
</script>
