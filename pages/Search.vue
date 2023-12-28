<template>
  <div class="select-partner">
    <el-container style="width:75%; justify-content: center; align-items: center; margin:auto">
      <el-main
        style="border-radius: 20px; margin:auto; border: 5px solid #C0C0C0"
      >
        <el-row>
          <el-col :span="6" class="grid" align="left">
            <span style="font-family: 'Times New Roman',serif;
               font-weight: bolder;
               font-size: 40px;
               color: #000">Find Partner</span>
          </el-col>
          <el-col :span="12" class="grid" align="left">
            <el-input placeholder="Search by student id or name…"
                      v-model="input"
                      prefix-icon="el-icon-search"
                      size="medium"
            >
            </el-input>
          </el-col>
          <el-col :span="6" class="grid" align="right">
            <el-button
              type="primary"
              icon="el-icon-s-operation"
              @click.native="openFilter()">
              Filter
            </el-button>
          </el-col>
        </el-row>
        <el-row :gutter="10" :justify="'center'" offset="10">
          <el-col :span="6" class="grid" v-for="(group,index) in groupShow" :key="index" align="middle">
            <el-card shadow="hover" @click.native="handleGroupCommand(group)"  :id="group.id">
              <div>
                <el-avatar :size="150" style="font-weight: bold;font-size: 40px" :src="group.avatar"></el-avatar>
              </div>
              <div style="font-family: '微软雅黑',serif; font-size: 40px;font-weight: bold; color:#F5F5DC;">
                <span>{{ group.name }}</span>
              </div>
              <div style="font-family: '微软雅黑',serif; font-size: 17px;font-weight: normal; color:#eee;">
                <span>{{ group.room }}</span>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <el-dialog
      title="Filter"
      :visible.sync="filterDialogVisible"
      width="50%"
      :before-close="closeFilter"
    >
      <el-form :model="newFilter" ref="newFilterForm" label-width="120px">
        <el-form-item
          label="Room Type"
          prop="room"
        >
          <el-select v-model="newFilter.room" placeholder="Select a room type">
            <el-option label="Male" value="male"></el-option>
            <el-option label="Female" value="female"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="Type"
          prop="type"
        >
          <el-select v-model="newFilter.type" placeholder="Select your identity">
            <el-option label="master" value="master"></el-option>
            <el-option label="PhD" value="PhD"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeCreateFilter">Cancel</el-button>
        <el-button
          type="danger"
          @click="clearFilterForm"
        >
          Clear
        </el-button>
        <el-button
          type="primary"
          @click="createNewFilter"
          :loading="loading"
        >
          OK
        </el-button>
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="ifOpenPersonDetail"
      custom-class="customDialog"
      :before-close="clearNew"
    >
      <el-main class="el-dialog__header">
        <el-row style="margin-top: 2px; margin-bottom: 2px">
          <el-col span="4" align="left">
            <el-avatar :size="150" style="font-weight: bold;font-size: 40px" :src="newGroup.avatar"></el-avatar>
          </el-col>
          <el-col span="18" align="left">
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <span style="font-family: 'Calibri',serif;
             font-weight: bolder;
             font-size: 40px;
             color: #000">{{newGroup.name}}</span>
            </el-row>
          </el-col>
        </el-row>
      </el-main>
      <el-main class="el-dialog__body">
        <el-row>
          <el-col span="4" align="center">
            <span style="font-size: 20px; font-weight: bold">GroupID:</span>
          </el-col>
          <el-col span="16" align="left">
            <span style="font-size: 18px;"> {{newGroup.id}}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col span="4" align="center">
            <div>
              <span style="font-size: 20px; font-weight: bold">Member:</span>
            </div>
          </el-col>
          <el-col span="3" v-for="(k, index) in newGroup.members" :key="index">
            <el-avatar :size="100" style="font-weight: bold;font-size: 40px" :src="k.avatar" align="center"></el-avatar>
            <div style="font-size: 18px;" align="center">{{ k.name }}</div>
          </el-col>
        </el-row>
      </el-main>

      <div align="center">
        <span slot="footer" class="dialog-footer">
          <el-button
            type="danger"
            @click="closeGroupDetail"
          >
            Done
          </el-button>
        </span>
      </div>

    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      groups: [
        {
          id: "100020231001",
          name: "sus",
          room: "Male",
          members: ["Alice", "Bob", "Charlie"],
        },
        {
          id: "200000150056",
          name: "dorm",
          room: "Male",
          members: ["David"],
        },
        {
          id: "356221002122",
          name: "developer",
          room: "Female",
          members: ["Grace", "Harry"],
        },
      ],
      newGroup: {
        id: '',
        avatar: '',
        name: '',
        habits: '',
        gender: '',
        day: '',
        contact: '',
        interests: '',
        team: null,
        degree: '',
      },
      newFilter: {
        room:"",
        type:"",
      },
      loading: false,
      input: '',
      filter:{
        room:"",
        type:"",
        isTrue: false,
      },
      ifOpenPersonDetail: false,
      ifOpenFilter: false,
    };
  },
  mounted() {
    this.getAllUser();
  },
  methods: {
    async getAllUser(){
      const apiUrl = 'https://backend.susdorm.online/api/all-profiles/';
      try {
        const response = await axios.get(apiUrl,);
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            id: list[i]['studentId'],
            avatar: list[i]['avatar'],
            name: list[i]['name'],
            habits: list[i]['habits'],
            gender: list[i]['sex'],
            day: list[i]['sleep'] + '-' + list[i]['wake'],
            contact: list[i]['contact'],
            interests: list[i]['interests'],
            team: list[i]['team'],
            degree: list[i]['degree'],
          };
        }
        this.groups = list;
        this.$message.success("success");
      } catch (error) {
        this.$message.error(error.toString());
        console.error('Error fetching files:', error);
      }
    },
    handleCommand() {
      this.createGroupDialogVisible = true;
    },
    handleGroupCommand(group){
      this.newGroup = {
        id: group.id,
        avatar: group.avatar,
        name: group.name,
        habits: group.habits,
        gender: group.gender,
        day: group.day,
        contact: group.contact,
        interests: group.interests,
        team: group.team,
        degree: group.degree,
      }
      this.isAbleApply = false;
      this.isAbleLeave = false;
      this.isAbleAdd = false;
      this.isAbleChat = false;
      this.isAbleEdit = false;
      this.isAbleDisband = false;
      this.isAbleChat = false;
      this.isAbleAdd = false;
      this.isAbleDelete = false;
      this.userType = "visitor"
      if (localStorage.getItem('pk') === this.newGroup.id){
        this.userType = "member";
      }
      if (this.localUser.id === this.newGroup.leaderId){
        this.userType = "creator";
      }
      if (this.userType === "visitor") {
        this.isAbleApply = group.members.length < 4;
      }
      else if (this.userType === "member") {
        this.isAbleLeave = true;
        this.isAbleChat = true;
      }
      else if (this.userType === "creator"){
        this.isAbleEdit = true;
        this.isAbleDisband = true;
        this.isAbleChat = true;
        this.isAbleAdd = true;
        this.isAbleDelete = true;
      }
      this.ifOpenPersonDetail = true;
    },
    openFilter() {
      this.filterDialogVisible = true;
    },
    clearFilterForm() {
      this.resetNewFilter();
    },
    closeFilter(done) {
      this.resetNewFilter();
      done();
    },
    handleClose(done){
      this.resetNewGroupForm();
      done();
    },
    clearNew(done){
      this.newGroup = {
        id: '',
        avatar: '',
        name: '',
        habits: '',
        gender: '',
        day: '',
        contact: '',
        interests: '',
        team: null,
        degree: '',
      };
      done();
    },
    handleClose_edit(done){
      this.resetNewGroupForm2();
      done();
    },
    editTeam(group){
      this.newGroup = group;
      this.openEditGroup();
    },
    openEditGroup(){
      this.editGroupDialogVisible = true;
    },
    chatGroup(row) {
      // TODO: implement the logic for chatting with a group
      alert("You are about to enter the chat room of " + row.name);
    },
    leaveGroup() {
      try{
        // 发送POST请求
        const response = axios.post('https://backend.susdorm.online/api/leave-team/', '');
        // 处理后端响应
        console.log('Backend Response:', response);
        this.$message.success("You left the team.");
      } catch (error) {
        // 处理请求错误
        console.error('Error sending data to backend:', error);
        this.$message.success("Some error evoked when you left the team.");
      }
      this.closeGroupDetail();
    },
    async joinGroup(id) {
      try{
        const dataToSend = {
          id: id,
        };
        // 发送POST请求
        const response = await axios.post('https://backend.susdorm.online/api/join-team/', dataToSend);
        if (response.status === 200){
          this.$message.success("Your application to this team had been sent.");
        }
        // 处理后端响应
        console.log('Backend Response:', response.data);
      } catch (error) {
        // 处理请求错误
        this.$message.error("ERROR: You cannot join this team due to gender or other reason.");
        console.error('Error sending data to backend:', error);
      }
      // alert("Your application for " + id + " has been sent.");
      this.closeGroupDetail();
    },
    async deleteGroup() {
      try{
        // 发送POST请求
        const response = await axios.post('https://backend.susdorm.online/api/leave-team/', '');
        // 处理后端响应
        console.log('Backend Response:', response.data);
        if (response.status === 200){
          this.$message.success("You disband your team.");
        }
      } catch (error) {
        // 处理请求错误
        console.error('Error sending data to backend:', error);
        this.$message.success("Some error evoked when you disband the team.");
      }
      this.closeGroupDetail();
    },
    closeCreateGroupDialog() {
      this.createGroupDialogVisible = false;
      this.resetNewGroupForm();
    },
    closeCreateFilter() {
      this.filterDialogVisible = false;
      this.clearFilterForm();
    },
    closeEditGroupDialog() {
      this.editGroupDialogVisible = false;
      this.resetNewGroupForm2();
    },
    closeGroupDetail() {
      this.ifOpenPersonDetail = false;
      this.newGroup = {
        id: '',
        avatar: '',
        name: '',
        habits: '',
        gender: '',
        day: '',
        contact: '',
        interests: '',
        team: null,
        degree: '',
      }
    },
    resetNewGroupForm() {
      this.$refs.newGroupForm.resetFields();
    },
    resetNewGroupForm2() {
      this.$refs.newGroupForm2.resetFields();
    },
    resetNewFilter() {
      this.$refs.newFilterForm.resetFields();
    },
    createNewFilter() {
      this.loading = true;
      //TODO: implement the logic for filtering
      this.filter = {room: this.newFilter.room, type:this.newFilter.type, isTrue: true}
      alert("You select " + this.newFilter.type + ", " + this.newFilter.room);
      this.closeCreateFilter()
      this.loading = false;
    },
    ifFilter(){

    },
    async createNewGroup() {
      this.$refs.newGroupForm.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          const dataToSend = {
            name: this.newGroup.name
          };
          // 发送POST请求
          axios.post('https://backend.susdorm.online/api/create-team/', dataToSend)
            .then(response => {
              console.log('Backend Response:', response.data);
              if (response.status === 200){
                this.$message.success("Your team had been created!")
              }
            })
            .catch(error => {
              // 处理错误
              this.$message.error("Some error evoked when you created the team.");
              console.error("Error:", error);
            });
          // 处理后端响应

          this.closeCreateGroupDialog();
          this.loading = false;
        } else {
          this.$message.error("Please fill in all the required fields.");
        }
      });
    },
    async editGroup() {
      this.$refs.newGroupForm2.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try{
            const dataToSend = {
              name: this.newGroup.name
            };
            // 发送POST请求
            const response = axios.post('https://backend.susdorm.online/api/update-team/', dataToSend);
            // 处理后端响应
            console.log('Backend Response:', response);
          } catch (error) {
            // 处理请求错误
            console.error('Error sending data to backend:', error);
          }
          this.closeEditGroupDialog();
          this.loading = false;
          this.closeGroupDetail();
        } else {
          this.$message.error("Please fill in all the required fields.");
        }
      });
    },
  },
  computed: {
    groupShow() {
      const input = this.input;

      if (input) {
        return this.groups.filter(groups => {
          return (
            (!this.filter.room || groups.room === this.filter.room) &&
            (!this.filter.type || groups.type === this.filter.type)
          ) && (
            Object.keys(groups).some(key => {
              return String(groups[key]).toLowerCase().indexOf(input.toLowerCase()) > -1;
            })
          );
        });
      }

      return this.groups.filter(groups => {
        return (
          (!this.filter.room || groups.room === this.filter.room) &&
          (!this.filter.type || groups.type === this.filter.type)
        );
      });
    }
  }
};
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  background-size: cover;
  color: #333;
  line-height: 60px;
}
.el-aside {
  background-color: #333;
}
.select-partner {
  margin-top: 20px;
}
.group-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.group-members {
  margin-top: 20px;
}
.member-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.el-card {
  margin-right: 20px;
  transition: all .5s;
  height: 300px;
  border-radius: 12px;
  background-color: #426B1F;
}
.el-card:hover{
//margin: 5px;
  padding-left: 10px;
}
.el-main {
  text-align: center;
}
.el-row {
  margin-top: 30px;
  margin-bottom: 20px;
}
</style>
<style>
.customDialog {
  background: #F5EFEC;
  width: 70%;
  height: 80%;
  border-radius: 20px;
}
</style>

