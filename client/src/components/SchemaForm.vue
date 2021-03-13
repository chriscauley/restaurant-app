<template>
  <ur-form v-if="schema" :schema="schema" v-bind="$attrs" :onSubmit="submit" />
</template>

<script>
import api from '@/common/api'

export default {
  props: {
    form_name: String,
  },
  computed: {
    schema() {
      return this.$store.schema.fetch(this.form_name)
    },
  },
  methods: {
    submit(state) {
      console.log(state)
      api.post(`schema/${this.form_name}/`, state)
    },
  },
}
</script>
