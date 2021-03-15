<template>
  <div class="modal">
    <div class="modal__mask" @click="close" />
    <div class="modal__content" :style="style">
      <div class="modal__title h4" v-if="title">
        {{ title }}
      </div>
      <div class="modal__body">
        <slot />
      </div>
      <div class="modal__footer">
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
    width: {
      type: [Number, String],
      default: 400,
    },
  },
  computed: {
    style() {
      return this.width ? `width: ${this.width}px` : ''
    },
  },
}
</script>
