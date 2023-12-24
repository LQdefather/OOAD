<template>
  <div class="select-group">
    <el-container style="width:75%; justify-content: center; align-items: center; margin:auto">
      <el-main
        style="border-radius: 20px; margin:auto; border: 5px solid #C0C0C0"
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
            <el-card shadow="hover" @click.native="handleCommand()">
              <div>
                <el-avatar :size="150" icon="el-icon-plus" style="font-size: 80px;"></el-avatar>
              </div>
              <div style="font-family: 'Calibri',serif; font-size: 28px;font-weight: normal; color:#eee;">
                <span>Create Your Group!</span>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6" class="grid" v-for="(group,index) in groupShow" :key="index" align="middle">
            <el-card shadow="hover" @click.native="handleGroupCommand(group)">
              <div>
                <el-avatar :size="150" style="font-weight: bold;font-size: 40px">Group</el-avatar>
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
        <el-form-item
          label="Description"
          prop="description"
          :rules="[{
            required: true,
            message: 'Please enter a group description',
            trigger: 'blur'
            }]"
        >
          <el-input v-model="newGroup.description"></el-input>
        </el-form-item>
        <el-form-item
          label="Room Type"
          prop="room"
          required
        >
          <el-select v-model="newGroup.room" placeholder="Select a room type">
            <el-option label="Single Room" value="Single Room"></el-option>
            <el-option label="Double Room" value="Double Room"></el-option>
            <el-option label="Triple Room" value="Triple Room"></el-option>
            <el-option label="Quadruple Room" value="Quadruple Room"></el-option>
          </el-select>
        </el-form-item>
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
            <el-option label="Single Room" value="Single Room"></el-option>
            <el-option label="Double Room" value="Double Room"></el-option>
            <el-option label="Triple Room" value="Triple Room"></el-option>
            <el-option label="Quadruple Room" value="Quadruple Room"></el-option>
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
      :visible.sync="ifOpenGroupDetail"
      custom-class="customDialog"
      :before-close="clearNew"
    >
      <el-main class="el-dialog__header">
        <el-row style="margin-top: 2px; margin-bottom: 2px">
          <el-col span="4" align="left">
            <el-avatar :size="120" style="font-size: 30px;">Group</el-avatar>
          </el-col>
          <el-col span="18" align="left">
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <span style="font-family: 'Calibri',serif;
             font-weight: bolder;
             font-size: 40px;
             color: #000">{{newGroup.name}}</span>
            </el-row>
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <span style="font-family: '微软雅黑', serif;
                font-weight: lighter;
                font-size: 18px;
                color: #000"
              >{{newGroup.description}}</span>
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
          <el-col span="2" align="left"  v-for="(k, index) in newGroup.members" :key="index">
            <li style="font-size: 18px;">{{ k }}</li>
          </el-col>
        </el-row>
      </el-main>

      <div align="center">
        <span slot="footer" class="dialog-footer">
          <el-button
            type="primary"
            icon="el-icon-s-home"
            @click="closeGroupDetail"
          >
            Chat
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
// axios.defaults.baseURL = '/proxy_url'
export default {
  data() {
    return {
      groups: [
        {
          id: "100020231001",
          name: "sus",
          room: "Quadruple Room",
          members: ["Alice", "Bob", "Charlie"],
          description: "welcome to our room!",
        },
        {
          id: "200000150056",
          name: "dorm",
          room: "Single Room",
          members: ["David"],
          description: "It's my room.",
        },
        {
          id: "356221002122",
          name: "developer",
          room: "Double Room",
          members: ["Grace", "Harry"],
          description: "No more request.",
        },
      ],
      createGroupDialogVisible: false,
      filterDialogVisible: false,
      ifOpenGroupDetail:false,
      newGroup: {
        id:"",
        name:"",
        room:"",
        members: [],
        description:"",
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
      }
    };
  },
  // devServer: {
  //   proxy: {
  //     '/getTeam': {
  //       target: 'http://localhost:8080/', // Replace with your Flask server address
  //       changeOrigin: true,
  //       ws: true,
  //     },
  //   },
  // },
  created() {
    this.getAllTeam();
  },
  methods: {

    async getAllTeam(){
      const apiUrl = 'http://localhost:8080/getTeam';
      try {
        const response = await axios.get(apiUrl,{
          headers: {
            token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InJvb3QifQ.0Ia3eD-FWd4Ik2bfP3AGoGjcpupkBqo9_OQqxWB9ksA"
          }
        });
        // console.log(response.data);
        this.groups = response.data;
        // let list = response.data;
        // for (let i = 0; i < list.length; i++) {
        //   const user = await this.getUserDetailsById(list[i].leaderId);
        //
        //   const combinedItem = {
        //     name: list[i].name,
        //     description: user.name,
        //   };
        //
        //   list[i] = combinedItem;
        // }
        // this.groups = list;
        this.$message.info("success");
      } catch (error) {
        this.$message.error(error.toString());
        console.error('Error fetching files:', error);
      }
    },
    handleCommand() {
      this.createGroupDialogVisible = true;
    },
    handleGroupCommand(group){
      this.newGroup = {id:group.id, name:group.name,
        description:group.description, room:group.room,
        members: group.members }
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
    chatGroup(row) {
      // TODO: implement the logic for chatting with a group
      alert("You are about to enter the chat room of " + row.name);
    },
    joinGroup(row) {
      // TODO: implement the logic for joining a group
      alert("Your application for " + row.name + " has been sent.");
    },
    deleteGroup(row) {
      // TODO: implement the logic for deleting a group
      alert("You deleted " + row.name);
    },
    closeCreateGroupDialog() {
      this.createGroupDialogVisible = false;
      this.resetNewGroupForm();
    },
    closeCreateFilter() {
      this.filterDialogVisible = false;
      this.clearFilterForm();
    },
    closeGroupDetail() {
      this.ifOpenGroupDetail = false;
      this.newGroup = {
        id:"",
        name:"",
        room:"",
        members: [],
        description:"",
      }
    },
    resetNewGroupForm() {
      this.$refs.newGroupForm.resetFields();
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
    async createNewGroup() {
      // TODO: implement the logic for creating a new group
      this.$refs.newGroupForm.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          let group = {
            id: "1001", name: this.newGroup.name,
            description: this.newGroup.description, room: this.newGroup.room,
            members: ["example_TBC"]
          };
          this.groups.push(group);
          let postData = {name:group.name, leaderId:1};
          const apiUrl = 'https://localhost:8080/createTeam';
          try {
            const res = await axios.post(apiUrl, postData, {
              headers: {
                "Content-Type": "application/json"
              },
            });
            console.log('Response from server:', res);
            // this.postResult = this.JSON.stringify(result, null, 2);
          } catch (err) {
            // this.postResult = this.JSON.stringify(err.response?.data, null, 2) || err;
            this.closeCreateGroupDialog();
            this.loading = false;
            this.$message.error(err.toString());
          }
          this.closeCreateGroupDialog();
          this.loading = false;
        } else {
          this.$message.error("Please fill in all the required fields.");
        }
      });
    },
  },
  computed: {
    groupShow() {
      const input = this.input
      if (input) {
        return this.groups.filter(data => {
          console.log("object:" + Object.keys(data))
          return Object.keys(data).some(key => {
            return String(data[key]).toLowerCase().indexOf(input) > -1
          })
        })
      }
      return this.groups
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

