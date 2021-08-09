<template>
  <navbar />
  <router-view class="router-view" />
  <ui />
  <story-card />
</template>

<script>
import { StoryCard } from '@unrest/story'
import Navbar from '@/components/Navbar'
import Ui from '@/components/Ui'

export default {
  components: { StoryCard, Navbar, Ui },
}
</script>
