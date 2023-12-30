<template>
  <div class="top-nav">
    <el-header class="header">
      <div class="nav-logo">
        <span class="nav-title">SUSDorm</span>
      </div>
    </el-header>
    <el-menu
      class="nav-menu"
      mode="horizontal"
      :default-active="activeIndex"
      @select="handleSelect"
    >
      <div class="nav-logo">
        <img src="/assets/logo.png" alt="Logo" class="logo-img"/>
      </div>
      <el-menu-item index="/person" class="el-menu-item">
        <i class="el-icon-house"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      <el-menu-item index="/Dorm" class="el-menu-item">
        <i class="el-icon-thumb"></i>
        <span slot="title">宿舍选择</span>
      </el-menu-item>
      <el-menu-item index="/DormView" class="el-menu-item">
        <i class="el-icon-menu"></i>
        <span slot="title">查看宿舍</span>
      </el-menu-item>
      <el-menu-item index="/Group" class="el-menu-item">
        <i class="el-icon-user"></i>
        <span slot="title">加入群组</span>
      </el-menu-item>
      <el-menu-item index="/Map" class="el-menu-item">
        <i class="el-icon-map-location"></i>
        <span slot="title">查看地图</span>
      </el-menu-item>
      <el-menu-item index="/chat" class="el-menu-item">
        <i class="el-icon-chat-dot-round"></i>
        <span slot="title">聊天室</span>
      </el-menu-item>
      <el-menu-item index="/Search" class="el-menu-item">
        <i class="el-icon-search"></i>
        <span slot="title">查找用户</span>
      </el-menu-item>
      <el-button icon="el-icon-message" class="message_button" circle @click="handleClick"></el-button>
      <div class="user-profile">
        <el-avatar class="avatar" :src="avatarUrl" alt="User Avatar"></el-avatar>
      </div>
    </el-menu>
    <el-dialog :visible.sync="dialogVisible" title="消息">
      <el-header>消息记录</el-header>
      <el-main>
        <el-timeline>
          <el-timeline-item
            v-for="message in allmessage"
            :key="message.id"
            :timestamp="message.created_at"
            placement="top">
            {{ message.content }}
          </el-timeline-item>
        </el-timeline>
      </el-main>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name:'choose',
  data() {
    return {
      activeIndex: '', // 当前选中的菜单项
      avatarUrl:'',
      dialogVisible: false,
      allmessage:null,
    };
  },
  mounted() {
    this.getAvatar();
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push(key);
      this.activeIndex = key;
    },
    getAvatar(){
      axios.get('https://backend.susdorm.online/api/get-avatar/', {withCredentials:true})
        .then((response) => {  // 使用箭头函数
          this.avatarUrl = response.data['avatar'];
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleClick() {
      // 点击图标时，显示弹窗
      axios.get('https://backend.susdorm.online/api/notifications/', {withCredentials:true})
        .then((response) => {  // 使用箭头函数
          this.allmessage = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
      this.dialogVisible = true;
    }

  }
};
</script>

<style scoped>
.top-nav {
  background-color: #333; /* 深色背景增强科技感 */
  color: #fff;
  /* 添加边框作为视觉点缀 */
}

.header {
  background-image: url('static/assets/bg.png'); /* 替换为您的图片路径 */
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-position: center; /* 背景图片居中 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 150px;
}

.nav-logo {
  display: flex;
  align-items: center;
  margin-right: auto;
  margin-left: 20px
}

.logo-img {
  height: 50px;
  margin-right: 10px;
}

.nav-title {
  font-size: 48px;
  font-weight: bold; /* 加粗字体 */
  color: #ffffff; /* 使用亮色调突出标题 */
}

.nav-menu {
  display: flex;
  align-items: center;
  background-color: #ffffff; /* 深色菜单背景 */
  justify-content: center;

}

.user-profile {
  display: flex;
  align-items: center;
  margin-left: auto;
  margin-right: 20px;
}

.el-menu-item {
  display: flex;
  align-items: center;
  margin: 0 10px; /* 增加菜单项间距 */
  color: rgba(170, 170, 170, 0.98); /* 菜单项使用亮色调 */
  font-weight: bold; /* 加粗字体 */
}

.el-menu-item:hover {
  color: #7baeef; /* 鼠标悬停时高亮显示 */
}

.el-icon {
  color: #4A90E2; /* 图标使用亮色调 */
  margin-right: 5px; /* 图标与文字间距 */
}

.message_button{
  margin-left: auto;
  margin-right: -110px;
}

</style>
