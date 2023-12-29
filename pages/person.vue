<template>
  <div class="profile">
    <!-- 个人信息展示部分 -->
    <choose/>
    <el-card class="info-card">
      <div slot="header" class="clearfix header-color">
        <span>个人信息</span>
      </div>
      <div>
        <el-avatar class="avatar" :src="avatarUrl" alt="User Avatar"></el-avatar>
      </div>
      <div class="profile-info">
        <div class="info">
          <p><strong>姓名:</strong> {{ userInfo.name }}</p>
          <p><strong>性别:</strong> {{ userInfo.gender }}</p>
          <p><strong>作息时间:</strong> {{ userInfo.day }}</p>
          <p><strong>个人简介:</strong> {{ userInfo.habits }}</p>
          <p><strong>联系方式:</strong> {{ userInfo.contact }}</p>
          <p><strong>兴趣爱好:</strong> {{ userInfo.interests }}</p>
        </div>
      </div>
      <el-button type="info" @click="showUploadAvatarDialog">上传头像</el-button>

      <!-- 修改信息按钮 -->
      <el-button type="primary" @click="showEditInfoDialog">修改信息</el-button>
      <el-button type="danger" @click="showChangePasswordDialog">修改密码</el-button>
    </el-card>
    <!-- 上传头像按钮 -->
    <basis/>

    <!-- 其他弹窗和逻辑保持不变 -->

    <!-- 修改信息弹窗 -->
    <el-dialog
      title="修改个人信息"
      :visible.sync="editInfoDialogVisible"
      width="50%"
    >
      <div class="edit-info-form">
        <el-form ref="editInfoForm" :model="editedUserInfo">
          <el-form-item label="睡觉时间" prop="sleep">
            <el-time-picker
              v-model="selectedTimeS"
              :picker-options="pickerOptions"
              format="HH:mm:ss"
              placeholder="选择时间">
            </el-time-picker>
          </el-form-item>
          <el-form-item label="起床时间" prop="wake">
            <el-time-picker
              v-model="selectedTimeW"
              :picker-options="pickerOptions"
              format="HH:mm:ss"
              placeholder="选择时间">
            </el-time-picker>
          </el-form-item>
          <el-form-item label="个人简介" prop="habits">
            <el-input type="textarea" v-model="editedUserInfo.habits"></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="contact">
            <el-input v-model="editedUserInfo.contact"></el-input>
          </el-form-item>
          <el-form-item label="兴趣爱好" prop="interests">
            <el-input v-model="editedUserInfo.interests"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelEditInfo">取消</el-button>
        <el-button type="primary" @click="saveEditedInfo">保存</el-button>
      </span>
    </el-dialog>

    <!-- 修改密码按钮 -->

    <!-- 修改密码弹窗 -->
    <el-dialog
      title="修改密码"
      :visible.sync="changePasswordDialogVisible"
      width="30%"
    >
      <div class="change-password-form">
        <el-form ref="changePasswordForm" :model="passwordChange">
          <el-form-item label="原密码" prop="old_password">
            <el-input type="password" v-model="passwordChange.old_password"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="password">
            <el-input type="password" v-model="passwordChange.password"></el-input>
          </el-form-item>
          <el-form-item label="确认新密码" prop="password2">
            <el-input type="password" v-model="passwordChange.password2"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelChangePassword">取消</el-button>
        <el-button type="primary" @click="saveChangedPassword">保存</el-button>
      </span>
    </el-dialog>

    <!-- 上传头像弹窗 -->
    <el-dialog
      title="上传头像"
      :visible.sync="uploadAvatarDialogVisible"
      width="30%"
    >
      <div class="upload-avatar-form">
        <el-upload
          class="avatar-uploader"
          action="/upload"
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="avatarPreview" :src="avatarPreview" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelUploadAvatar">取消</el-button>
        <el-button type="primary" @click="uploadAvatar">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      pickerOptions: {
        selectableRange: '00:00:00 - 23:59:59'
      },
      avatarUrl: '',
      userInfo: {
        name: 'John Doe',
        gender: 'Male',
        day: '11:00-7:00',
        contact: 'john.doe@example.com',
        habits: 'Hello, I am John Doe.',
        interests: [],
      },
      avatarPreview: null,
      editInfoDialogVisible: false,
      selectedFile: null,
      selectedTimeS: null,
      selectedTimeW: null,
      editedUserInfo: {
        wake: '',
        sleep:'',
        contact: '',
        habits: '',
        interests: [],
      },
      changePasswordDialogVisible: false,
      passwordChange: {
        old_password: '',
        password: '',
        password2: '',
      },
      uploadAvatarDialogVisible: false,
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    formatTime(time) {
      // 格式化时间为 HH:mm:ss 字符串
      const hours = time.getHours().toString().padStart(2, '0');
      const minutes = time.getMinutes().toString().padStart(2, '0');
      const seconds = time.getSeconds().toString().padStart(2, '0');
      return `${hours}:${minutes}:${seconds}`;
    },
    getUserInfo(){
      axios.get('https://backend.susdorm.online/api/user-information?pk=' + localStorage.getItem('pk'))
        .then((response) => {  // 使用箭头函数
          this.avatarUrl = response.data[0]['avatar']; // this 现在正确指向 Vue 实例
          this.userInfo.name = response.data[0]['name'];
          this.userInfo.contact = response.data[0]['contact'];
          this.userInfo.gender = response.data[0]['sex'];
          this.userInfo.interests = response.data[0]['interests'];
          this.userInfo.day = response.data[0]['sleep']+'-'+response.data[0]['wake'];
          this.userInfo.habits = response.data[0]['habits'];

        })
        .catch(function (error) {
          console.log(error);
        });
    },
    showEditInfoDialog() {
      this.editInfoDialogVisible = true;
      // 将用户信息复制到编辑表单中

    },
    cancelEditInfo() {
      this.editInfoDialogVisible = false;
    },
    saveEditedInfo() {
      // 在这里保存修改后的用户信息
      this.editedUserInfo.wake = this.formatTime(this.selectedTimeW)
      this.editedUserInfo.sleep = this.formatTime(this.selectedTimeS)
      axios.post('https://backend.susdorm.online/api/change-profile/', this.editedUserInfo)
        .then(response => {
          // 处理响应
          alert('修改成功');
        })
        .catch(error => {
          // 处理错误
          console.error("Error:", error);
        });
      this.getUserInfo();
      this.editInfoDialogVisible = false;
    },
    showChangePasswordDialog() {
      this.changePasswordDialogVisible = true;
    },
    cancelChangePassword() {
      this.changePasswordDialogVisible = false;
    },
    saveChangedPassword() {
      // 在这里保存修改后的密码
      axios.put('https://backend.susdorm.online/api/change-password/'+localStorage.getItem('pk')+'/', this.passwordChange)
        .then(response => {
          // 处理响应
          alert('修改成功');
        })
        .catch(error => {
          // 处理错误
          console.error("Error:", error);
        });
      this.changePasswordDialogVisible = false;
    },
    showUploadAvatarDialog() {
      this.uploadAvatarDialogVisible = true;
    },
    cancelUploadAvatar() {
      this.uploadAvatarDialogVisible = false;
      this.avatarPreview = null;
      this.selectedFile = null;
    },
    beforeAvatarUpload(file) {
      const isImage = file.type.startsWith('image/');
      if (!isImage) {
        this.$message.error('您只能上传图片文件！');
        return false;
      }

      const isLt2M = file.size / 1024 / 1024 < 20;
      if (!isLt2M) {
        this.$message.error('上传的图片大小不能超过 20MB！');
        return false;
      }

      // 创建一个 URL 用于预览
      this.avatarPreview = URL.createObjectURL(file);
      this.selectedFile = file;
      return false; // 阻止 el-upload 自动上传
    },
    uploadAvatar() {
      if (!this.selectedFile) {
        this.$message.error('请先选择一个文件');
        return;
      }

      const formData = new FormData();
      formData.append('avatar', this.selectedFile);

      axios.post('https://backend.susdorm.online/api/change-avatar/', formData)
        .then(response => {
          // 处理响应
          alert("修改成功")
          this.getUserInfo();
        })
        .catch(error => {
          // 处理错误
          console.error("Error:", error);
        });

      // 关闭对话框
      this.uploadAvatarDialogVisible = false;
    },
  },
};
</script>

<style scoped>
.profile {
  text-align: center;
  padding: 20px;
}

.info-card {
  width: 40%;
  margin: auto; /* Center card in the middle of the page */
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); /* Slight shadow for depth */
  margin-top: 30px;
  margin-bottom: 50px;
}

.profile-info {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin-bottom: 40px;
}

.avatar {
  width: 120px;
  height: 120px;
  border: 2px solid #f2f2f2; /* Slight border around avatar for depth */
  margin-right: 20px;
}

.info {
  text-align: left;
}

.info p {
  line-height: 1.5; /* More readable line spacing */
  margin: 0 0 10px 0; /* Space out the paragraphs */
}

/* Adjustments for buttons */
.el-button {
  margin: 10px 5px;
}

.header-color {
  background-color: #ffffff; /* 替换为你想要的颜色 */
}
</style>
