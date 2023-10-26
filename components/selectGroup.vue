<template>
  <div class="selectGroup">
    <el-container style="border: 1px solid #eee">
      <!--      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">-->
      <!--        <el-menu :default-openeds="['1', '3']">-->
      <!--          <el-submenu index="1">-->
      <!--            <template slot="title"><i class="el-icon-message"></i>1</template>-->
      <!--            <el-menu-item-group>-->
      <!--              <template slot="title">1</template>-->
      <!--              <el-menu-item index="1-1">1.1</el-menu-item>-->
      <!--              <el-menu-item index="1-2">1.2</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-menu-item-group title="2">-->
      <!--              <el-menu-item index="1-3">1.3</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-submenu index="1-4">-->
      <!--              <template slot="title">1.4</template>-->
      <!--              <el-menu-item index="1-4-1">1.4.1</el-menu-item>-->
      <!--            </el-submenu>-->
      <!--          </el-submenu>-->
      <!--          <el-submenu index="2">-->
      <!--            <template slot="title"><i class="el-icon-menu"></i>2</template>-->
      <!--            <el-menu-item-group>-->
      <!--              <template slot="title">2.1</template>-->
      <!--              <el-menu-item index="2-1">2.1.1</el-menu-item>-->
      <!--              <el-menu-item index="2-2">2.1.2</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-menu-item-group title="2.2">-->
      <!--              <el-menu-item index="2-3">2.2.3</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-submenu index="2-4">-->
      <!--              <template slot="title">2.2.4</template>-->
      <!--              <el-menu-item index="2-4-1">2.2.4-1</el-menu-item>-->
      <!--            </el-submenu>-->
      <!--          </el-submenu>-->
      <!--          <el-submenu index="3">-->
      <!--            <template slot="title"><i class="el-icon-setting"></i>3</template>-->
      <!--            <el-menu-item-group>-->
      <!--              <template slot="title">3.1</template>-->
      <!--              <el-menu-item index="3-1">3.1.1</el-menu-item>-->
      <!--              <el-menu-item index="3-2">3.1.2</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-menu-item-group title="3.2">-->
      <!--              <el-menu-item index="3-3">3.2.3</el-menu-item>-->
      <!--            </el-menu-item-group>-->
      <!--            <el-submenu index="3-4">-->
      <!--              <template slot="title">3.2.4</template>-->
      <!--              <el-menu-item index="3-4-1">3.2.4-1</el-menu-item>-->
      <!--            </el-submenu>-->
      <!--          </el-submenu>-->
      <!--        </el-menu>-->
      <!--      </el-aside>-->

      <el-container>
        <el-header
          style="text-align: right; font-size: 12px;width: 80%; margin:auto"
        >
          <el-dropdown trigger="click" @command = "handleCommand">
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command= "create">New Group</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>Example</span>
        </el-header>
        <el-main
          style="width: 80%; margin:auto"
        >
          <el-col :span="6" class="grid">
            <el-input placeholder="Search by group id or name…"
                      v-model="input"
                      prefix-icon="el-icon-search"
                      size="mini"
            >
            </el-input>
          </el-col>
          <el-table
            ref="groupsTable"
            :data="groupShow"
            stripe
          >
            <el-table-column prop="id" label="Group ID"></el-table-column>
            <el-table-column prop="name" label="Group Name"></el-table-column>
            <el-table-column
              prop="room"
              label="Group Room"
              :filters="[{ text: 'Single Room', value: 'Single Room' },
               { text: 'Double Room', value: 'Double Room' },
               { text: 'Triple Room', value: 'Triple Room' },
               { text: 'Quadruple Room', value: 'Quadruple Room' } ]"
              :filter-method="filterHandler"
            ></el-table-column>
            <el-table-column prop="members" label="Group Members">
              <template #default="{ row }">
                <el-tag v-for="member in row.members" :key="member">{{ member }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="Group Actions" type="action">
              <template #default="{ row }">
                <el-button-group>
                  <el-button
                    type="primary"
                    icon="el-icon-s-promotion"
                    @click.stop="chatGroup(row)"
                  >
                    Chat
                  </el-button>

                  <el-button
                    type="success"
                    icon="el-icon-circle-plus-outline"
                    @click.stop="joinGroup(row)"
                  >
                    Join
                  </el-button>

                  <el-button
                    type="danger"
                    icon="el-icon-delete"
                    @click.stop="deleteGroup(row)"
                    disabled
                  >
                    Delete
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
            <el-table-column type="expand">
              <template #default="{ row }">
                <el-descriptions class="margin-top" title="Group Detail" :column="1">
                  <el-descriptions-item label="Description">{{row.description}}</el-descriptions-item>
                  <el-descriptions-item label="**">*****</el-descriptions-item>
                  <el-descriptions-item label="**">*****</el-descriptions-item>
                </el-descriptions>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
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
  </div>
</template>

<script>
export default {
  name: 'selectGroup',
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
      newGroup: {
        id:"",
        name:"",
        room:"",
        members: [],
        description:"",
      },
      loading: false,
      input: '',
      // img: require('@/assets/header1.jpg'),
    };
  },
  methods: {
    handleCommand(command) {
      this.createGroupDialogVisible = true;
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
    resetNewGroupForm() {
      this.$refs.newGroupForm.resetFields();
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
    filterHandler(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    },
    clearFilter() {
      this.$refs.groupsTable.clearFilter();
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
  color: #333;
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
</style>


