<template>
  <div class="loginBody">
    <div class="loginDiv">
      <div class="login-content">
        <h1 class="login-title">用户登录</h1>
        <el-form :model="loginForm" label-width="100px"
                 :rules="rules" ref="loginForm">
          <el-form-item label="名字" prop="name">
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
import {client} from "/client"
import VueCookies from 'vue-cookies'
import { wrapper } from 'axios-cookiejar-support';
import { CookieJar } from 'tough-cookie';
Vue.use(VueCookies);

// const jar = new CookieJar();
// const client = wrapper(axios.create({ jar }));
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
  // proxy: {
  //   '/api': {
  //     target: 'https://backend.susdorm.online',  // Replace with your Django server URL
  //     changeOrigin: true,
  //   },
  // },
  methods:{
    confirm(){
      axios.post('https://backend.susdorm.online/api/login/', this.loginForm,
      )
        .then(response => {
          // 处理响应
          console.log(response.data)
          // this.$cookies.set('sessionid', response.data.sessionid, '7d','/','backend.susdorm.online',null,'Lax');
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
.loginBody {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}
.loginDiv {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -200px;
  margin-left: -250px;
  width: 450px;
  height: 360px;
  background: #b3d1c8;
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
