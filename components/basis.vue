<template>
  <el-header class="el-header">
  </el-header>
</template>

<script>
export default {
  name: "basis"
}
</script>

<style scoped>
.el-header{
  background-image: url('static/assets/bg3.png'); /* 替换为您的图片路径 */
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-position: center; /* 背景图片居中 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 150px;
}
</style>
