<template>
  <navbar />
  <router-view class="router-view" />
  <unrest-ui />
  <story-card />
</template>

<script>
import { StoryCard } from '@unrest/story'
import Navbar from '@/components/Navbar'

export default {
  components: { StoryCard, Navbar },
}
</script>
