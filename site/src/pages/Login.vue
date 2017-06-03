<template lang="pug">
  #login-sign
    mu-tabs(:value="activeTab", @change="handleTabChange")
      mu-tab(value="login", title="登录")
      mu-tab(value="sign", title="注册")
    mu-content-block.login-wrapper(v-if="activeTab==='login'")
      mu-text-field(label="用户名", hintText="请输入用户名/手机号", type="text", :labelFloat="true", :fullWidth="true", v-model="loginName")
      mu-text-field(label="密码", hintText="请输入密码", type="password", :labelFloat="true", :fullWidth="true", v-model="loginPwd")
      mu-raised-button.submit-btn(label="登录", primary, @click="submitLogin")
    mu-content-block.sign-wrapper(v-if="activeTab==='sign'")
      mu-text-field(label="手机号", hintText="请输入手机号", type="text", :labelFloat="true", :fullWidth="true", v-model="signPhone")
      .verify-code-wrapper
        .input
          mu-text-field(label="输入验证码", hintText="输入验证码", type="text", :labelFloat="true", :fullWidth="true", v-model="code")
        .send-btn
          mu-flat-button(:label="btnText || '发送验证码'", primary, @click="getVertifyCode" :backgroundColor="btnBg || '#7fc660'" color="#FFF")
      mu-text-field(label="昵称", hintText="请输入昵称", type="text", :labelFloat="true", :fullWidth="true", v-model="signName")
      mu-text-field(label="密码", hintText="请输入密码", type="password", :labelFloat="true", :fullWidth="true", v-model="signPwd")
      mu-text-field(label="确认密码", hintText="确认密码", type="password", :labelFloat="true", :fullWidth="true", v-model="signRePwd")
      mu-raised-button.submit-btn(label="注册", primary, @click="submitSign")
</template>

<script>
import API from '@/scripts/api'

export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loginName: '',
      loginPwd: '',
      signName: '',
      signPhone: '',
      signPwd: '',
      signRePwd: '',
      code: null,
      errorTip: '',
      btnBg: '#7fc660',
      btnText: '发送验证码',
    }
  },
  methods: {
    handleTabChange(val) {
      this.activeTab = val
    },
    getVertifyCode() {
      const phoneExp = /^1[3|4|5|7|8][0-9]{9}$/
      const phoneNum = this.signPhone
      let time = 60

      if (!phoneExp.test(phoneNum)) {
        this.$tip('请输入正确的手机号')
        return
      } else if (this.btnBg !== '#7fc660') {
        return
      }
      const setBtnForbidden = () => {
        this.btnBg = 'rgb(220,220,220)'
        this.btnText = `${time}s`
        time -= 1
        if (time > 0) setTimeout(setBtnForbidden, 1000)
        else {
          this.btnBg = null
          this.btnText = null
        }
      }
      this.$post(API.getVertifyCode, {
        phone_num: phoneNum,
      }).then(() => setBtnForbidden())
    },
    submitLogin() {
      const { loginName, loginPwd } = this
      this.$post(API.login, {
        phone_num: loginName,
        password: loginPwd,
      })
    },
    submitSign() {
      const { signPwd, signName, signRePwd, code, signPhone } = this
      if (!signPwd || !signName || !signRePwd) {
        this.$tip('还有未填完的选项喔')
        return
      } else if (signPwd !== signRePwd) {
        this.$tip('两次密码不一致')
      } else if (signPwd.length > 20) {
        this.$tip('密长度超过20个字符')
      }
      this.$post(API.sign, {
        phone_num: signPhone,
        password: signPwd,
        nickname: signName,
        verify_code: code,
      }).then(() => this.$tip('注册成功'))
    },
  },
}
</script>

<style lang='scss' scoped>
.verify-code-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .input {
    flex: 1;
  }
  .send-btn {
    flex: 0;
    white-space: nowrap;
  }
}
</style>

