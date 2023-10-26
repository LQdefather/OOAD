<template>
  <div class="main">
    <h1>Welcome to My App</h1>
    <p>Choose an option:</p>

    <!-- 第一个Element UI按钮 -->
    <el-button type="primary" @click="handleOption1">学生登录</el-button>

    <!-- 第二个Element UI按钮 -->
    <el-button type="success" @click="handleOption2">管理员端</el-button>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  methods: {
    handleOption1() {
      // 处理第一个按钮的点击事件
      this.$router.push('/login')
      // 在这里添加处理逻辑
    },
    handleOption2() {
      // 处理第二个按钮的点击事件
      this.$message.success('Option 2 Clicked');
      // 在这里添加处理逻辑
    },
  },
};
</script>

<style scoped>
.main {
  text-align: center;
  padding: 20px;
}
</style>

