<template>
  <div>
    <router-view class="app-view" />
  </div>
</template>

<script>
import RestaurantList from '@/components/RestaurantList'
export default {
  components: { RestaurantList },
}
</script>
