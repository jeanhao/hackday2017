
/*
手机类，包含一些基本方法和静态数据
 */
export default class Mobile {
  constructor() {
    const docEle = document.documentElement
    this.docEle = docEle
    this.mbWidth = docEle.clientWidth
    this.mbHeight = docEle.clientHeight
  }
  setFontSize() {
    // 动态改变根节点字体大小
    const curWidth = this.mbWidth
    const curHeight = this.mbHeight

    // 以iphone6尺寸为标准对照尺寸
    const ip6Width = 375
    const ip6Height = 603  // 屏幕高度应为667，但除去微信64px后即为64

    const scale = (curWidth / curHeight) / (ip6Width / ip6Height);

    const fontSize = curWidth / (ip6Width * scale * 0.01)
    this.docEle.style.fontSize = `${fontSize}px`
  }
}
