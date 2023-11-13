<template>
  <div class="top-nav">
    <!-- 顶部导航栏 -->
    <el-header>
      <!-- 导航栏标题 -->
      <div class="nav-title">
        <span>Dormitory Selection System</span>
      </div>
      <!-- 导航栏菜单 -->
      <el-menu
        class="nav-menu"
        mode="horizontal"
        :default-active="activeIndex"
        @select="handleSelect"
      >
        <el-menu-item index="/person">
          <i class="el-icon-house"></i>
          <span slot="title">首页</span>
        </el-menu-item>
        <el-menu-item index="/Dorm">
          <i class="el-icon-info"></i>
          <span slot="title">宿舍选择</span>
        </el-menu-item>
        <el-menu-item index="/DormView">
          <i class="el-icon-search"></i>
          <span slot="title">查看宿舍</span>
        </el-menu-item>
        <el-menu-item index="/Group">
          <i class="el-icon-phone"></i>
          <span slot="title">加入群聊</span>
        </el-menu-item>
        <el-menu-item index="/Map">
          <i class="el-icon-phone"></i>
          <span slot="title">查看地图</span>
        </el-menu-item>
      </el-menu>
    </el-header>
  </div>
</template>

<script>
export default {
  name:'choose',
  data() {
    return {
      activeIndex: '', // 当前选中的菜单项
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push(key);
      this.activeIndex = key;
    }
  }
};
</script>

<style scoped>
.top-nav {
  background-color: #4B4A4AFF;
  color: #fff;
}

.nav-title {
  font-size: 24px;
  padding: 20px 0;
  text-align: center;
}

.nav-menu {
  text-align: center;
}
</style>
