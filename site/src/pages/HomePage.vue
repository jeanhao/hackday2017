<template lang="pug">
#index-wrapper
  .plants-wrapper
     Slider(:pages="pages", :sliderinit="sliderinit")
</template>

<script>
import API from '@/scripts/api'
import Slider from '@/components/slider'

export default {
  name: 'HomePage',
  data() {
    return {
      pages: [
        {
          nickname: '小明一号',
        },
        {
          nickname: '石楠二号',
        },
        {
          nickname: '大仁三号',
        },
        {
          nickname: '夏浩四号',
        },
        {
          nickname: '曾豪五号',
        },
      ],
      sliderinit: {
        currentPage: 0,
        thresholdDistance: 50,
        thresholdTime: 500,
        autoplay: false,
        loop: false,
        direction: 'horizon',
        infinite: 1,
        slidesToScroll: 1,
      },
    }
  },
  mounted() {
    this.$get(API.plantList).then((res) => {
      this.pages = res
      if (!res || res.length === 0) {
        console.log(this.$router.go({ path: '/new' }))
      }
    })
  },
  components: {
    Slider,
  },
  methods: {
  },
}
</script>

<style lang='scss' scoped>
</style>
