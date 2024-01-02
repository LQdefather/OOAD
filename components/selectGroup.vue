<template>
  <div class="select-group">
    <el-container style="width:75%; justify-content: center; align-items: center; margin:auto">
      <el-main
        style="margin:auto; border: 0px"
      >
        <el-row>
          <el-col :span="6" class="grid" align="left">
            <span style="font-family: 'Times New Roman',serif;
               font-weight: bolder;
               font-size: 40px;
               color: #000">Joined Group</span>
          </el-col>
          <el-col :span="12" class="grid" align="left">
            <el-input placeholder="Search by group id or name…"
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
          <el-col :span="6" class="grid" >
            <el-card shadow="hover" @click.native="handleCommand()" style="margin-top: 20px; margin-bottom: 20px">
              <div>
                <el-avatar :size="150" icon="el-icon-plus" style="font-size: 80px;"></el-avatar>
              </div>
              <div style="font-family: 'Calibri',serif; font-size: 28px;font-weight: normal; color:#000;">
                <span>Create Your Group!</span>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6" class="grid" v-for="(group,index) in groupShow" :key="index" align="middle">
            <el-card shadow="hover" @click.native="handleGroupCommand(group)"  :id="group.id" style="margin-top: 20px; margin-bottom: 20px">
              <div>
                <el-avatar :size="150" style="font-weight: bold;font-size: 40px" :src="group.avatar"></el-avatar>
              </div>
              <div style="font-family: '微软雅黑',serif; font-size: 40px;font-weight: bold; color:#000;">
                <span>{{ group.name }}</span>
              </div>
              <div style="font-family: '微软雅黑',serif; font-size: 17px;font-weight: normal; color:#323131;">
                <span>{{ group.room }}</span>
                <span>{{ group.type }}</span>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <el-dialog
      title="Create a Group"
      :visible.sync="createGroupDialogVisible"
      width="50%"
      :before-close="handleClose"
    >
      <el-form :model="newGroup" ref="newGroupForm" label-width="120px">
        <el-form-item
          label="Group Name"
          prop="name"
          :rules="[{
            required: true,
            message: 'Please enter a group name',
            trigger: 'blur'
            }]"
        >
          <el-input v-model="newGroup.name"></el-input>
        </el-form-item>
<!--        <el-form-item-->
<!--          label="Room Type"-->
<!--          prop="room"-->
<!--          required-->
<!--        >-->
<!--          <el-select v-model="newGroup.room" placeholder="Select a room type">-->
<!--            <el-option label="Single Room" value="Single Room"></el-option>-->
<!--            <el-option label="Double Room" value="Double Room"></el-option>-->
<!--            <el-option label="Triple Room" value="Triple Room"></el-option>-->
<!--            <el-option label="Quadruple Room" value="Quadruple Room"></el-option>-->
<!--          </el-select>-->
<!--        </el-form-item>-->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeCreateGroupDialog">Cancel</el-button>
        <el-button
          type="primary"
          @click="createNewGroup"
          :loading="loading"
        >
          OK
        </el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="Edit a Group"
      :visible.sync="editGroupDialogVisible"
      width="50%"
      :before-close="handleClose_edit"
    >
      <el-form :model="newGroup" ref="newGroupForm2" label-width="120px">
        <el-form-item
          label="Group Name"
          prop="name"
          :rules="[{
            required: true,
            message: 'Please enter a group name',
            trigger: 'blur'
            }]"
        >
          <el-input v-model="newGroup.name"></el-input>
        </el-form-item>
<!--        <el-form-item-->
<!--          label="Description"-->
<!--          prop="description"-->
<!--          :rules="[{-->
<!--            required: true,-->
<!--            message: 'Please enter a group description',-->
<!--            trigger: 'blur'-->
<!--            }]"-->
<!--        >-->
<!--          <el-input v-model="newGroup.description"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item-->
<!--          label="Room Type"-->
<!--          prop="room"-->
<!--          required-->
<!--        >-->
<!--          <el-select v-model="newGroup.room" placeholder="Select a room type">-->
<!--            <el-option label="Single Room" value="Single Room"></el-option>-->
<!--            <el-option label="Double Room" value="Double Room"></el-option>-->
<!--            <el-option label="Triple Room" value="Triple Room"></el-option>-->
<!--            <el-option label="Quadruple Room" value="Quadruple Room"></el-option>-->
<!--          </el-select>-->
<!--        </el-form-item>-->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeEditGroupDialog()">Cancel</el-button>
        <el-button
          type="primary"
          @click="editGroup"
          :loading="loading"
        >
          OK
        </el-button>
      </span>
    </el-dialog>
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
            <el-option label="PhD" value="doctor"></el-option>
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
      :visible.sync="ifOpenGroupDetail"
      custom-class="customDialog"
      :before-close="clearNew"
    >
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
          <el-row style="margin-top: 2px; margin-bottom: 2px" v-if="isAbleChat">
            <el-col span="4" align="left">
              <span style="font-size: 20px; font-family: '微软雅黑', serif; color: #000" class="el-icon-star-on">Collected:</span>
            </el-col>
            <el-col span="16" align="left">
              <el-row style="margin-top: 2px; margin-bottom: 2px">
                <el-col :span="8" class="grid" v-for="(room,index) in bookmark" :key="index" align="middle">
                  <el-card shadow="hover" :id="room.id" style="margin-top: 2px; margin-bottom: 2px; height: 80px; border-radius: 2px; border: 0px; background-color: #f8f5f3">
                    <div style="font-family: '微软雅黑', serif; font-size: 20px; font-weight: bold; color:#000;">
                      <span>{{ room.roomNumber }}</span>
                    </div>
                    <div style="font-family: '微软雅黑', serif; font-size: 10px; font-weight: normal; color:#323131;">
                      <span>{{ room.zone }}</span>
                      <span>{{ room.building }}</span>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </el-col>
      </el-row>

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


      <div align="center">
        <span slot="footer" class="dialog-footer">
<!--          <el-button-->
<!--            type="info" icon="el-icon-chat-dot-round"-->
<!--            @click="closeGroupDetail"-->
<!--            v-if="isAbleChat"-->
<!--          >-->
<!--            Chat-->
<!--          </el-button>-->
          <el-button
            type="warning"
            icon="el-icon-s-release"
            @click="deleteGroup"
            v-if="isAbleDisband"
          >
            Disband
          </el-button>
          <el-button
            type="warning"
            icon="el-icon-user"
            @click="leaveGroup"
            v-if="isAbleLeave"
          >
            Leave
          </el-button>
          <el-button
            type="primary"
            icon="el-icon-edit-outline"
            @click="editTeam(newGroup)"
            v-if="isAbleEdit"
          >
            Edit
          </el-button>
<!--          <el-button-->
<!--            type="primary"-->
<!--            icon="el-icon-star-off"-->
<!--            @click="closeGroupDetail"-->
<!--            v-if="isAbleAdd"-->
<!--          >-->
<!--            Favor-->
<!--          </el-button>-->
<!--          <el-button-->
<!--            type="danger"-->
<!--            icon="el-icon-remove-outline"-->
<!--            @click="closeGroupDetail"-->
<!--            v-if="isAbleDelete"-->
<!--          >-->
<!--            Remove Favor-->
<!--          </el-button>-->
          <el-button
            type="success"
            icon="el-icon-tickets"
            @click="joinGroup(newGroup.id)"
            v-if="isAbleApply"
          >
            Apply
          </el-button>
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
      localUser: {
        id: "",
        gender: "",
        type: "",
        team: 0,
      },
      groups: [
        // {
        //   id: "100020231001",
        //   name: "sus",
        //   room: "Male",
        //   members: ["Alice", "Bob", "Charlie"],
        // },
        // {
        //   id: "200000150056",
        //   name: "dorm",
        //   room: "Male",
        //   members: ["David"],
        // },
        // {
        //   id: "356221002122",
        //   name: "developer",
        //   room: "Female",
        //   members: ["Grace", "Harry"],
        // },
      ],
      userType: "visitor",
      createGroupDialogVisible: false,
      editGroupDialogVisible: false,
      filterDialogVisible: false,
      ifOpenGroupDetail:false,
      isAbleEdit: false,
      isAbleDisband: false,
      isAbleChat: false,
      isAbleAdd: false,
      isAbleDelete: false,
      isAbleLeave: false,
      isAbleApply: false,
      newGroup: {
        id:"",
        name:"",
        room:"",
        type:"",
        members: [],
        leaderId: "",
        avatar: "",
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
      bookmark:[],
    };
  },
  mounted() {
    this.getUserInfo();
    this.getAllTeam();
    this.getOwnBookmark();
  },
  methods: {
    async getOwnBookmark(){
      try {
        const response = await axios.get('https://backend.susdorm.online/api/bookmark-dorms/',{ withCredentials: true });
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            id :list[i]['id'],
            type: list[i]['type'],
            zone: list[i]['zone'],
            roomNumber:list[i]['roomNumber'],
            building:list[i]['building'],
            roomLayout: list[i]['roomLayout']
          };
        }
        this.bookmark = list;
        // this.$message.success("success");
      } catch (error) {
        this.$message.error(error.toString());
        console.log(error);
      }
    },
    async getUserInfo(){
      axios.get('https://backend.susdorm.online/api/user-information/?pk=' + localStorage.getItem('pk'),{ withCredentials: true })
        .then((response) => {  // 使用箭头函数
          // this.avatarUrl = response.data[0]['avatar']; // this 现在正确指向 Vue 实例
          this.localUser.id = response.data[0]['studentId'];
          this.localUser.gender = response.data[0]['sex'];
          this.localUser.type = response.data[0]['degree'];
          this.localUser.team = response.data[0]['team'];
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    async getAllTeam(){
      const apiUrl = 'https://backend.susdorm.online/api/teams/';
      try {
        const response = await axios.get(apiUrl,);
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            id: list[i]['id'],
            name: list[i]['name'],
            room: list[i]['leader']['sex'],
            type: list[i]['leader']['degree'],
            members: list[i]['members'],
            leaderId: list[i]['leader']['studentId'],
            avatar: list[i]['leader']['avatar'],
            pk: list[i]['leader']['pk']
          };
        }
        this.groups = list;
        // this.$message.success("success");
      } catch (error) {
        this.$message.error(error.toString());
        console.error('Error fetching files:', error);
      }
    },
    handleCommand() {
      this.createGroupDialogVisible = true;
    },
    handleGroupCommand(group){
      this.newGroup = {id:group.id, name:group.name, type:group.type, avatar: group.avatar,
        room:group.room, members: group.members, leaderId: group.leaderId}
      this.isAbleApply = false;
      this.isAbleLeave = false;
      this.isAbleAdd = false;
      this.isAbleChat = false;
      this.isAbleEdit = false;
      this.isAbleDisband = false;
      this.isAbleAdd = false;
      this.isAbleDelete = false;
      this.userType = "visitor"
      if (this.localUser.team === this.newGroup.id){
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
      this.ifOpenGroupDetail = true;
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
        id:"",
        name:"",
        room:"",
        type:"",
        members: [],
        leaderId: "",
        avatar: "",
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
        const response = axios.post('https://backend.susdorm.online/api/leave-team/', '',{withCredentials:true});
        // 处理后端响应
        console.log('Backend Response:', response);
        window.location.href = window.location.href
        this.$message.success("You left the team.");
      } catch (error) {
        // 处理请求错误
        console.error('Error sending data to backend:', error);
        this.$message.error("Some error evoked when you left the team.");
      }
      this.closeGroupDetail();
    },
    async joinGroup(id) {
      try{
        const dataToSend = {
            id: id,
        };
        // 发送POST请求
        const response = await axios.post('https://backend.susdorm.online/api/join-team/', dataToSend,{withCredentials:true});
        // 处理后端响应
        console.log('Backend Response:', response.data);
        if (response.status === 200){
          window.location.href = window.location.href
          // this.$message.success("Your application to this team had been sent.");
        }
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
        const response = await axios.post('https://backend.susdorm.online/api/leave-team/', '',{withCredentials:true});
        // 处理后端响应
        console.log('Backend Response:', response.data);
        if (response.status === 200){
          window.location.href = window.location.href
          this.$message.success("You disband your team.");
        }
      } catch (error) {
        // 处理请求错误
        console.error('Error sending data to backend:', error);
        this.$message.error("Some error evoked when you disband the team.");
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
      this.ifOpenGroupDetail = false;
      this.newGroup = {
        id:"",
        name:"",
        room:"",
        type:"",
        members: [],
        leaderId: "",
        avatar: "",
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
      let flag = false
      this.$refs.newGroupForm.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try {
            const dataToSend = {
              name: this.newGroup.name
            };
            // 发送POST请求
            const response = axios.post('https://backend.susdorm.online/api/create-team/', dataToSend, {withCredentials: true});
            console.log('Backend Response:', response);
            this.$message.success("Your team had been created!")
            flag = true
          }catch(error) {
                // 处理错误
                this.$message.error("Some error evoked when you created the team.");
                console.error("Error:", error);
              }
            // 处理后端响应

          this.closeCreateGroupDialog();
          this.loading = false;
        } else {
          this.$message.error("Please fill in all the required fields.");
        }
      });
      if (flag){
        window.location.href = window.location.href
      }
    },
    async editGroup() {
      let flag = false
      this.$refs.newGroupForm2.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try{
            const dataToSend = {
              name: this.newGroup.name
            };
            // 发送POST请求
            const response = axios.post('https://backend.susdorm.online/api/update-team/', dataToSend,{withCredentials:true});
            // 处理后端响应
            console.log('Backend Response:', response);
            flag = true
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
      if (flag){
        window.location.href = window.location.href
      }
    },
    getImageSrc(type) {
      // Add your logic here to determine the image source based on the type
      if (type === 'quadruple_room') {
        return require('../static/dorm/dorm1.jpg');
      } else if (type === 'single_room') {
        return require('../static/dorm/dorm2.jpg');
      }else if(type === 'double_room'){
        return require('../static/dorm/dorm3.jpg');

      }
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
.select-group {
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
  border-radius: 8px;
  //background-color: #eeeeee;
  border: 3px solid #173a3e;
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
.card-content-container:hover{
  padding-right: 10px;
}
</style>
<style>
.image {
  width: 100%;
  display: block;
}
.customDialog {
  background: #F5EFEC;
  width: 70%;
  height: 80%;
  border-radius: 20px;
}
.mycard {
  position: relative
}
.mycard .word {
  position: absolute;
  left: 25px;
  top: 250px;
  width: 275px;
  height: 265px;
  box-sizing: border-box;
  padding: 10px;background:rgba(0,0,0,.5)
}
</style>

