<template>
  <div class="background-image-container">
    <div class = "title-con"><h1 class="title">SUSDorm</h1></div>
    <div class="main">
      <!-- 第一个Element UI按钮 -->
      <el-button type="primary" @click="handleOption1">学生登录</el-button>
      <el-button type="primary" @click="handleOption1">用户手册</el-button>
      <!-- 第二个Element UI按钮 -->
    </div>
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
  },
};
</script>

<style scoped>
.background-image-container {
  background-image: url('static/assets/bg2.png');
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-position: center; /* 背景图片居中 */
  padding: 390px;
}
.main {
  text-align: center;
  padding: 20px;
}
.title-con{
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
}
.title{
  font-size: 80px;
  color: #ffffff;
}

</style>

