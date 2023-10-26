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
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editedUserInfo.name"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-input v-model="editedUserInfo.gender"></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="contact">
            <el-input v-model="editedUserInfo.contact"></el-input>
          </el-form-item>
          <el-form-item label="个人简介" prop="bio">
            <el-input type="textarea" v-model="editedUserInfo.bio"></el-input>
          </el-form-item>
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
          <el-form-item label="原密码" prop="oldPassword">
            <el-input type="password" v-model="passwordChange.oldPassword"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input type="password" v-model="passwordChange.newPassword"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelChangePassword">取消</el-button>
        <el-button type="primary" @click="saveChangedPassword">保存</el-button>
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
