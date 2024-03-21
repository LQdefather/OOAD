<template>
  <div class="background-image-container">
    <div class = "title-con"><h1 class="title">SUSDorm</h1></div>
    <div class="main">
      <!-- 第一个Element UI按钮 -->
      <el-button type="primary" @click="handleOption1">学生登录</el-button>
      <el-button type="primary" @click="handleOption2">用户手册</el-button>
      <!-- 第二个Element UI按钮 -->
    </div>
    <el-dialog
      title="南科大学生组队选宿舍系统用户手册"
      :visible.sync="dialogVisible"
      width="70%">

      <!-- 用户手册的内容 -->
      <div class="user-manual-content">
        <h3>1. 登录</h3>
        <p>账号与密码：用户可以使用已注册的账号和初始密码进行登录。</p>

        <h3>2. 个人信息</h3>
        <h4>2.1 查看个人信息</h4>
        <p>登录后，用户可以查看自己的个人信息，包括学号、姓名等基本信息。</p>
        <h4>2.2 个人信息编辑</h4>
        <p>在个人信息界面，用户可以进行以下操作：</p>
        <ul>
          <li>上传头像</li>
          <li>更改密码</li>
          <li>设置作息时间</li>
          <li>添加个人简介</li>
          <li>添加兴趣爱好标签</li>
        </ul>

        <h3>3. 查看宿舍</h3>
        <h4>3.1 宿舍信息</h4>
        <p>在宿舍界面，用户可以筛选、查看宿舍的详细信息。</p>
        <h4>3.2 用户互动</h4>
        <p>用户可以进行以下互动操作：</p>
        <ul>
          <li>发表评论</li>
          <li>为宿舍打分</li>
          <li>收藏宿舍（每个团队的收藏上限为5个）</li>
        </ul>

        <h3>4. 宿舍选择</h3>
        <h4>4.1 时间限制</h4>
        <p>用户可以在规定的时间内为自己的团队选择宿舍。</p>

        <h3>5. 加入群组</h3>
        <h4>5.1 团队操作</h4>
        <p>在群组界面，用户可以进行以下操作：</p>
        <ul>
          <li>查看、加入、创建团队</li>
          <li>查看自己团队的收藏宿舍</li>
        </ul>
        <h4>5.2 团队聊天</h4>
        <p>用户加入团队后，可以参与团队聊天，查看团队的历史聊天记录。请注意，聊天室只能在加入团队后才能使用。</p>

        <h3>6. 查看地图</h3>
        <h4>6.1 宿舍位置</h4>
        <p>在地图界面，用户可以查看各个宿舍的位置，并可以从自己的位置开始导航到目的地宿舍。</p>

        <h3>7. 聊天室</h3>
        <h4>7.1 团队聊天</h4>
        <p>用户在加入团队后可以使用聊天室功能，参与团队聊天，以及查看团队的历史聊天记录。请注意，聊天室只能在加入团队后才能使用。</p>

        <h3>8. 查找用户</h3>
        <h4>8.1 查找同伴</h4>
        <p>用户可以通过输入学号、姓名的方式查找对应同伴，也可以通过标签、作息时间等信息筛选同伴。</p>
        <h4>8.2 联系同伴</h4>
        <p>用户可以查看同伴的个人信息与联系方式，进行有效沟通。</p>
        <h4>8.3 历史评论记录</h4>
        <p>用户可以查看同伴的历史评论记录，以便更好地了解同伴的宿舍偏好与评价。</p>

        <p><strong>注意：</strong>用户必须拥有团队后才能进行宿舍选择和团队聊天操作。</p>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      // 控制对话框显示的变量
      dialogVisible: false,
    };
  },
  methods: {
    handleOption1() {
      // 处理第一个按钮的点击事件
      this.$router.push('/login')
      // 在这里添加处理逻辑
    },
    handleOption2() {
      // 处理第一个按钮的点击事件
      this.dialogVisible=true
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
 .user-manual-content {
   /* 添加你的样式 */
   line-height: 1.6;
 }

.user-manual-content h3 {
  margin-top: 20px;
}

.user-manual-content h4 {
  margin-top: 10px;
}

.dialog-footer {
  text-align: right;
}

</style>

