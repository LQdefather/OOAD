<template>
  <div class="loginBody">
    <div class="loginDiv">
      <div class="login-content">
        <h1 class="login-title">用户登录</h1>
        <el-form :model="loginForm" label-width="100px"
                 :rules="rules" ref="loginForm">
          <el-form-item label="名字" prop="name">
            <el-input style="width: 200px" type="text" v-model="loginForm.name"
                      autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input style="width: 200px" type="password" v-model="loginForm.password"
                      show-password autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="身份" prop="identity">
            <el-select style="width: 200px" type="text" v-model="loginForm.identity" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="confirm">确 定</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data(){
    return{
      loginForm:{
        name:'',
        password:'',
        identity:''
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
      if(this.loginForm.identity == 1)
      this.$router.replace('/person');
      else if(this.loginForm.identity == 2)
        this.$message.error("请从管理员端登录！");
      else this.$message.error("请选择身份！");
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
  height: 430px;
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
</style>
