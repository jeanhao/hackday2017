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
      mu-text-field(label="用户名", hintText="请输入用户名/手机号", type="text", :labelFloat="true", :fullWidth="true", v-model="signName")
      mu-text-field(label="密码", hintText="请输入密码", type="password", :labelFloat="true", :fullWidth="true", v-model="signPwd")
      mu-text-field(label="确认密码", hintText="确认密码", type="password", :labelFloat="true", :fullWidth="true", v-model="signRePwd")
      mu-raised-button.submit-btn(label="注册", primary, @click="submitSign")
    mu-popup(position="top", :overlay="false", :open="!!errorTip") {{errorTip}}
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loginName: '',
      loginPwd: '',
      signName: '',
      signPwd: '',
      signRePwd: '',
      errorTip: '',
    }
  },
  methods: {
    handleTabChange(val) {
      this.activeTab = val
    },
    submitLogin() {
      const { loginName, loginPwd } = this
      this.$post('/login', {
        name: loginName,
        pwd: loginPwd,
      }).catch((err) => {
        console.log(err)
      })
    },
    submitSign() {
      const { signPwd, signName, signRePwd } = this
      if (!signPwd || !signName || !signRePwd) {
        this.errorTip = '还有未填完的选项喔'
        setTimeout(() => {
          this.errorTip = null
        }, 2000)
      }
      this.$post('/sign', {
        name: signName,
        pwd: signPwd,
      })
    },
  },
}
</script>

<style lang='scss'>
.header {
  background-color: red;
}
</style>

