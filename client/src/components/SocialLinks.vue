<template>
  <div class="social-links">
    <div class="social-links__or">Or {{ verb }} With</div>
    <div class="social-links__links">
      <div v-for="social in socials" :key="social.slug">
        <a :class="`btn -${social.slug}`" :href="social.href">
          <i :class="`fa fa-${social.slug} mr-2`" />
          {{ social.name }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    verb: String,
  },
  computed: {
    socials() {
      return this.$store.auth.social
    },
  },
}
</script>
