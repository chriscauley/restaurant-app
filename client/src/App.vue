<template>
  <navbar />
  <router-view class="router-view" />
  <ui />
</template>

<script>
import Navbar from '@/components/Navbar'
import Ui from '@/components/Ui'

export default {
  components: { Navbar, Ui },
}
</script>
