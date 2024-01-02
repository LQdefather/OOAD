<template>
  <div>
    <div>
      <choose/>
    </div>
    <div class="bg">
      <el-card class="chat-room">
        <div class="message-container">
          <!-- 更新消息布局，移除头像和名字 -->
          <div v-for="message in messages" :key="message.id" class="message-card" :class="{'self-message': message.currentUser}">
            <!-- 仅在消息不是当前用户发出时显示用户名 -->
            <div class="message-timestamp">{{ formattedTime(message.time) }}</div>
            <div v-if="!message.currentUser" class="message-header">
              <img :src="message.avatar" class="user-avatar"/>
              <span class="user-name">{{ message.trueName }}:</span>
            </div>
            <div class="message-content">{{ message.text }}</div>
          </div>
        </div>
        <div class="input-container">
          <el-input v-model="currentMessage" placeholder="输入消息..." @keyup.enter="sendMessage"></el-input>
          <el-button type="primary" @click="sendMessage">发送</el-button>
        </div>
      </el-card>
    </div>
    <div>
      <basis/>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'ChatRoom',
  data() {
    return {
      currentMessage: '',
      messages: [],
    };
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get('https://backend.susdorm.online/api/messages/',{withCredentials:true}
        );
        this.messages = response.data;
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    async sendMessage() {
      if (this.currentMessage.trim() === '') {
        return;
      }
      try {
        const response = await axios.post('https://backend.susdorm.online/api/send-message/', {
          text: this.currentMessage,
        },{withCredentials:true});
        this.messages.push(response.data);
        this.currentMessage = '';
        this.fetchMessages();
      } catch (error) {
        console.error('Error sending message:', error);
      }
    },
    formattedTime(timestamp) {
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
  },
};
</script>

<style scoped>
.chat-room {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  margin-top: 80px;
  margin-bottom: 80px;
}

.message-container {
  height: 500px;
  overflow-y: auto;
  margin-bottom: 20px;
  margin-top: 20px;
}

.message-card {
  margin-bottom: 10px;
  word-break: break-word;
}

.input-container {
  display: flex;
  justify-content: space-between;
}

.input-container .el-input {
  margin-right: 10px;
  flex-grow: 1;
}

.message-header {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 15px;
  margin-right: 10px;
}

.user-name {
  font-weight: bold;
}

.message-content {
  margin-top: 5px;
}

.self-message .message-header {
  display: none; /* 不显示当前用户的名字和头像 */
}

/* 更新自己消息的样式，使其右对齐且不显示名字 */
.self-message {
  text-align: right;
  margin-right: 20px;
}

.self-message .message-content {
  display: inline-block;
  background-color: rgb(170, 200, 236); /* 或者你喜欢的颜色 */
  padding: 10px;
  border-radius: 10px;
}

/* 调整其他人消息的样式 */
.message-card:not(.self-message) .message-content {
  display: inline-block;
  background-color: rgba(226, 226, 226, 0.99); /* 或者你喜欢的颜色 */
  padding: 10px;
  border-radius: 10px;
}

.message-timestamp {
  color: #a0a0a0;  /* 时间戳字体颜色 */
  font-size: 0.8em; /* 时间戳字体大小 */
  margin-right: 10px; /* 与消息内容的间距 */
  text-align: center;
}

.chat-header {
  background-color: rgb(75, 74, 74); /* 背景颜色 */
  color: white; /* 字体颜色 */
  padding: 10px; /* 内边距 */
  font-size: 1.2em; /* 字体大小 */
  text-align: center; /* 文本居中 */
  border-top-left-radius: 4px; /* 顶部左边角圆角 */
  border-top-right-radius: 4px; /* 顶部右边角圆角 */
}

.bg {
  background-image: url('static/assets/bg7.jpg'); /* 替换为您的图片路径 */
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-position: center; /* 背景图片居中 */
  padding: 100px;
}

</style>
