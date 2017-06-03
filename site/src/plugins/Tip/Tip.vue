<template>
  <transition name="fade" appear v-on:after-enter="afterEnter">
    <div class="tip-container" v-if="msg">
      {{ msg }}
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
    }
  },
}
</script>
<style lang='scss' scoped>
.tip-container{
  position: fixed;
  left: 50%;
  top: 10px;
  transform: translateX(-50%);
  z-index: 9999;
  margin: auto;
  display: inline-block;
  text-align: center;
  font-size: 14px;
  color: #fff;
  padding: 6px 12px;
  background: rgba(255,0,51,0.5);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s ease, top .5s ease;
}
.fade-enter, .fade-leave-active {
  top: -100px;
  opacity: 0;
}
</style>
