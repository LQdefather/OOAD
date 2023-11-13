<template>
  <div class="profile">
    <!-- 个人信息展示部分 -->
    <choose/>
    <div class="profile-info">
      <el-avatar class="avatar" :src="avatarUrl" alt="User Avatar"></el-avatar>
      <div class="info">
        <p><strong>姓名:</strong> {{ userInfo.name }}</p>
        <p><strong>性别:</strong> {{ userInfo.gender }}</p>
        <p><strong>联系方式:</strong> {{ userInfo.contact }}</p>
        <p><strong>个人简介:</strong> {{ userInfo.bio }}</p>
      </div>
    </div>

    <!-- 上传头像按钮 -->
    <el-button type="info" @click="showUploadAvatarDialog">上传头像</el-button>

    <!-- 修改信息按钮 -->
    <el-button type="primary" @click="showEditInfoDialog">修改信息</el-button>

    <!-- 修改信息弹窗 -->
    <el-dialog
      title="修改个人信息"
      :visible.sync="editInfoDialogVisible"
      width="50%"
    >
      <div class="edit-info-form">
        <el-form ref="editInfoForm" :model="editedUserInfo">
          <!-- ... 其他表单项 ... -->
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelEditInfo">取消</el-button>
        <el-button type="primary" @click="saveEditedInfo">保存</el-button>
      </span>
    </el-dialog>

    <!-- 修改密码按钮 -->
    <el-button type="danger" @click="showChangePasswordDialog">修改密码</el-button>

    <!-- 修改密码弹窗 -->
    <el-dialog
      title="修改密码"
      :visible.sync="changePasswordDialogVisible"
      width="30%"
    >
      <div class="change-password-form">
        <el-form ref="changePasswordForm" :model="passwordChange">
          <!-- ... 其他表单项 ... -->
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
        <!-- 这里添加上传头像的表单或组件 -->
        <!-- 例如，可以使用 <el-upload> 组件来实现文件上传 -->
        <!-- 注意更新 avatarUrl 的值 -->
        <el-upload
          class="avatar-uploader"
          action="/upload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="avatarUrl" :src="avatarUrl" class="avatar">
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
export default {
  data() {
    return {
      avatarUrl: 'https://example.com/avatar.jpg',
      userInfo: {
        name: 'John Doe',
        gender: 'Male',
        contact: 'john.doe@example.com',
        bio: 'Hello, I am John Doe.',
      },
      editInfoDialogVisible: false,
      editedUserInfo: {
        name: '',
        gender: '',
        contact: '',
        bio: '',
      },
      changePasswordDialogVisible: false,
      passwordChange: {
        oldPassword: '',
        newPassword: '',
      },
      uploadAvatarDialogVisible: false,
    };
  },
  methods: {
    showEditInfoDialog() {
      this.editInfoDialogVisible = true;
      // 将用户信息复制到编辑表单中
      this.editedUserInfo = { ...this.userInfo };
    },
    cancelEditInfo() {
      this.editInfoDialogVisible = false;
    },
    saveEditedInfo() {
      // 在这里保存修改后的用户信息
      this.userInfo = { ...this.editedUserInfo };
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
      this.passwordChange.oldPassword = '';
      this.passwordChange.newPassword = '';
      this.changePasswordDialogVisible = false;
    },
    showUploadAvatarDialog() {
      this.uploadAvatarDialogVisible = true;
    },
    cancelUploadAvatar() {
      this.uploadAvatarDialogVisible = false;
    },
    handleAvatarSuccess(response, file) {
      // 上传成功后更新 avatarUrl 的值
      this.avatarUrl = response.url;
    },
    beforeAvatarUpload(file) {
      // 验证上传的文件格式等
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }

      return isJPG && isLt2M;
    },
    uploadAvatar() {
      // 在这里实现上传头像的逻辑
      // 可以使用第三方库或服务，也可以直接调用后端接口
      // 在上传成功后，更新 avatarUrl 的值
      // this.avatarUrl = '新的头像地址';
      this.uploadAvatarDialogVisible = false;
    },
  },
};
</script>

<style scoped>

.profile {
  text-align: center;
  padding: 10px;
}

.profile-info {
  text-align: center;
  padding: 120px;
}

.avatar {
  width: 100px;
  height: 100px;
  margin-right: 20px;
}

.info {
  text-align: left;
  display: inline-block;
  vertical-align: top;
}

.edit-info-form,
.change-password-form {
  padding: 20px;
}
</style>
