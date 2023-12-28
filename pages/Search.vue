<template>
  <div>
    <div>
      <choose/>
    </div>
    <el-card class="chat-room">
      <div class="message-container">
        <!-- 更新消息卡片以包括头像和用户名 -->
        <el-card v-for="message in messages" :key="message.id" class="message-card" :class="{'self-message': message.isSelf}">
          <div class="message-header">
            <img :src="message.avatar" class="user-avatar"/>
            <span class="user-name">{{ message.username }}:</span>
          </div>
          <div class="message-content">{{ message.text }}</div>
        </el-card>
      </div>
      <div class="input-container">
        <el-input v-model="currentMessage" placeholder="输入消息..." @keyup.enter="sendMessage"></el-input>
        <el-button type="primary" @click="sendMessage">发送</el-button>
      </div>
    </el-card>
  </div>
</template>


<script>
export default {
  data() {
    return {
      messages: [
        { sender: 'User', text: 'Hello!' },
        { sender: 'Bot', text: 'Hi there!' },
      ],
      newMessage: '',
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage) {
        this.messages.push({ sender: 'User', text: this.newMessage });
        // 模拟异步回复
        setTimeout(() => {
          this.messages.push({ sender: 'Bot', text: 'I received your message!' });
        }, 500);
        this.newMessage = '';
      }
    },
  },
};
</script>
