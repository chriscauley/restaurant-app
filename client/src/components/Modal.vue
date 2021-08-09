<template>
  <div class="modal">
    <div class="modal-mask" @click="close" />
    <div class="modal-content">
      <div class="modal-title h4" v-if="title">
        {{ title }}
      </div>
      <div class="modal-body">
        <slot />
      </div>
      <div class="modal-footer">
        <slot name="actions">
          <button class="btn -secondary" @click="close">Close</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    close: Function,
    title: String,
  },
}
</script>
