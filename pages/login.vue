<template>
  <div class="background-image-container">
    <div class="logo">

    </div>
    <div class="loginDiv">
      <div class="login-content">
        <h1 class="login-title">用户登录</h1>
        <el-form :model="loginForm" label-width="100px"
                 :rules="rules" ref="loginForm">
          <el-form-item label="学号" prop="name">
            <el-input style="width: 200px" type="text" v-model="loginForm.username"
                      autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input style="width: 200px" type="password" v-model="loginForm.password"
                      show-password autocomplete="off" size="small"></el-input>
          </el-form-item>
          <div class="login_button">
            <el-button type="primary" @click="confirm">确 定</el-button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>

import Vue from "vue";
import axios from "axios";
import VueCookies from 'vue-cookies'
Vue.use(VueCookies);
export default {
  name: "login",
  data(){
    return{
      loginForm:{
        username:'',
        password:'',
      },
      options: [
        { value: '1', label: '学生' },
        { value: '2', label: '老师' },
      ],
      rules:{

      }
    }
  },
  methods:{
    confirm(){
      axios.post('https://backend.susdorm.online/api/login/', this.loginForm,

        )
        .then(response => {
          // 处理响应
          // this.$cookies.set('sessionid', response.data.sessionid, '7d')
          document.cookie = 'sessionid=' + response.data.sessionid
          // this.$cookies.set('sessionid', response.data.sessionid, '7d','/', 'www.susdorm.online',true, 'None')
          alert(response.data.sessionid)

          localStorage.setItem('pk', response.data.pk);
          this.$router.replace('/person');
        })
        .catch(error => {
          // 处理错误
          console.error("Error:", error);
        });
       // this.$router.replace('/person');

    }
  }
}
</script>

<style scoped >
.background-image-container {
  background-image: url('static/assets/bg2.png');
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-position: center; /* 背景图片居中 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 430px;
}
.loginDiv {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -200px;
  margin-left: -230px;
  width: 450px;
  height: 360px;
  background-color: rgba(232, 229, 229, 0.8); /* 设置背景透明度为 0.5 */
  border-radius: 5%;
}
.login-title {
  margin: 20px 0;
  text-align: center;
}
.login-content {
  width: 400px;
  height: 250px;
  position: absolute;
  top: 25px;
  left: 25px;
}
.login_button{
  text-align: center;
}
</style>
