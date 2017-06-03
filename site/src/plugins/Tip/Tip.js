import TipProto from './Tip.vue'

export default {
  install(Vue) {
    const TipConstructor = Vue.extend(TipProto)
    let TipInstance = null
    const body = document.getElementsByTagName('body')[0]

    const Fun = (msg, callback) => {
      if (TipInstance) {
        TipInstance.msg = msg
        return
      }
      TipInstance = new TipConstructor({
        el: document.createElement('div'),
        data() {
          return {
            msg,
          }
        },
        methods: {
          afterEnter() {
            if (this.msg) setTimeout(() => { this.msg = null }, 2500)
          },
        },
        // 挂载，类似vue1.0中的ready
        mounted() {
          this.$nextTick(() => {
            body.appendChild(this.$el)
          })
          setTimeout(() => { this.msg = null }, 2500)
        },
      })
      if (callback) {
        setTimeout(() => {
          if (callback) callback()
        }, 1000)
      }
    }

    /* eslint-disable no-param-reassign */
    Vue.prototype.$tip = Fun
    Vue.$tip = Fun
    /* eslint-enable no-param-reassign */
  },
}
