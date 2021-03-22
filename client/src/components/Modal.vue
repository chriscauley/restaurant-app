<template>
  <div class="modal">
    <div class="modal__mask" @click="close" />
    <div class="modal__content">
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
  },
}
</script>
