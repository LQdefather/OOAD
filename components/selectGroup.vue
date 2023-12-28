<template>
  <div class="select-group">
    <el-container style="width:75%; justify-content: center; align-items: center; margin:auto">
      <el-main
        style="border-radius: 20px; margin:auto; border: 5px solid #C0C0C0"
      >
        <el-row>
          <el-col :span="6" class="grid" align="left">
          <span style="font-family: 'Ink Free',serif;
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
              <div style="font-family: 'MV Boli',serif; font-size: 28px;font-weight: normal; color:#eee;">
                <span>Create Your Group!</span>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6" class="grid" v-for="(group,index) in groupShow" :key="index" align="middle">
            <el-card shadow="hover" @click.native="handleGroupCommand(group)">
              <div>
                <el-avatar :size="150" style="font-weight: bold;font-size: 40px">Group</el-avatar>
              </div>
              <div style="font-family: 'MV Boli',serif; font-size: 40px;font-weight: bold; color:#F5F5DC;">
                <span>{{ group.name }}</span>
              </div>
              <div style="font-family: 'Times New Roman',serif; font-size: 17px;font-weight: normal; color:#eee;">
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
    >
      <el-container>
        <el-col span="6" align="center">
          <el-avatar :size="100" style="font-size: 20px;">Group</el-avatar>
        </el-col>
        <el-main>{{newGroup.name}}</el-main>
      </el-container>
      <el-row>
        <span>{{newGroup.id}}</span>
      </el-row>
      <el-row>
        <span>{{newGroup.description}}</span>
      </el-row>
      <el-row>
        <span>{{newGroup.members}}</span>
      </el-row>
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
    </el-dialog>
  </div>
</template>

<script>
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
    };
  },
  methods: {
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
      let filter = {room: this.newFilter.room, type:this.newFilter.type}
      alert("You select " + this.newFilter.type + ", " + this.newFilter.room);
      this.closeCreateFilter()
      this.loading = false;
    },
    createNewGroup() {
      // TODO: implement the logic for creating a new group
      this.$refs.newGroupForm.validate((valid) => {
        if (valid) {
          this.loading = true;
          let group = {id:"1001", name:this.newGroup.name,
            description:this.newGroup.description, room:this.newGroup.room,
            members: ["example_TBC"] };
          this.groups.push(group);
          this.closeCreateGroupDialog();
          this.loading = false;
          alert("You created a new group with name " + group.name);
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

