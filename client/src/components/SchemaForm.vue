<template>
  <ur-form v-if="schema" :schema="schema" v-bind="$attrs" :onSubmit="submit" :errors="errors" />
  <div v-else class="ur-placeholder" />
</template>

<script>
import api from '@/common/api'
import { cloneDeep } from 'lodash'

export const prepSchema = schema => {
  schema = cloneDeep(schema)
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
}

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
      const schema = this.$store.schema.fetch(this.form_name)
      if (!schema) {
        return
      }
      return prepSchema(schema)
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
        .post(`${this.form_name}/`, state)
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
