<template>
  <div class="select-partner">
    <choose/>
    <el-container style="width:75%; justify-content: center; align-items: center; margin:auto; margin-top: 30px">
      <el-main
        style="border-radius: 20px; margin:auto; border: 0px"
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
              <div style="font-family: '微软雅黑',serif; font-size: 40px;font-weight: bold; color:#000;">
                <span>{{ group.name }}</span>
              </div>
              <div style="font-family: '微软雅黑',serif; font-size: 17px;font-weight: normal; color:#323131;">
                <span>{{ group.gender }}</span>
                <span>{{ group.degree }}</span>
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
          label="Gender"
          prop="gender"
        >
          <el-select v-model="newFilter.gender" placeholder="Select gender">
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
        <el-checkbox-group v-model="newFilter.tag" size="small" :min="0" :max="5">
          <el-checkbox v-for="(tag,index) in this.all_tag" :label="tag.name" :key="tag">
            {{tag.name.length > 5 ? tag.name.substring(0, 5) + '...': tag.name}}
          </el-checkbox>
        </el-checkbox-group>
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
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <el-col span="4" align="left">
                <span style="font-size: 20px; font-weight: bold; font-family: '微软雅黑', serif; color: #000">Contact:</span>
              </el-col>
              <el-col span="14" align="left">
                <span style="font-family: '微软雅黑', serif;
                  font-size: 18px;
                  color: #000"
                >{{newGroup.contact}}</span>
              </el-col>
            </el-row>
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <el-col span="4" align="left">
                <span style="font-size: 20px; font-weight: bold; font-family: '微软雅黑', serif; color: #000">Gender:</span>
              </el-col>
              <el-col span="14" align="left">
                <span style="font-family: '微软雅黑', serif;
                  font-size: 18px;
                  color: #000"
                ><i v-if="newGroup.gender === 'male'" class="el-icon-male"></i>
                <i v-if="newGroup.gender === 'female'" class="el-icon-female"></i></span>
              </el-col>
            </el-row>
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <el-col span="4" align="left">
                <span style="font-size: 20px; font-weight: bold; font-family: '微软雅黑', serif; color: #000">Degree:</span>
              </el-col>
              <el-col span="14" align="left">
                <span style="font-family: '微软雅黑', serif;
                  font-size: 18px;
                  color: #000"
                >{{newGroup.degree}}</span>
              </el-col>
            </el-row>
            <el-row style="margin-top: 2px; margin-bottom: 2px">
              <el-col span="4" align="left">
                <span style="font-size: 20px; font-weight: bold; font-family: '微软雅黑', serif; color: #000">Team:</span>
              </el-col>
              <el-col span="14" align="left">
                <span style="font-family: '微软雅黑', serif;
                  font-size: 18px;
                  color: #000"
                >{{newGroup.team}}</span>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </el-main>
      <el-main class="el-dialog__body">
        <el-row>
          <el-col span="4" align="center">
            <span style="font-size: 20px; font-weight: bold">StudentID:</span>
          </el-col>
          <el-col span="16" align="left">
            <span style="font-size: 18px;"> {{newGroup.id}}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col span="4" align="center">
            <span style="font-size: 20px; font-weight: bold">Schedule:</span>
          </el-col>
          <el-col span="16" align="left">
            <span style="font-size: 18px;"> {{newGroup.day}}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col span="4" align="center">
            <span style="font-size: 20px; font-weight: bold">Description:</span>
          </el-col>
          <el-col span="16" align="left">
            <span style="font-size: 18px;"> {{newGroup.habits}}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col span="4" align="center">
            <div>
              <span style="font-size: 20px; font-weight: bold">Interest:</span>
            </div>
          </el-col>
          <el-col span="2" v-for="(k, index) in newGroup.interests" :key="index">
            <el-tag type="danger" style="font-size: 18px;" align="center">{{ k }}</el-tag>
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
    <div class="bot">
      <basis/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      all_tag: [],
      groups: [],
      newGroup: {
        id: '',
        avatar: '',
        name: '',
        habits: '',
        gender: '',
        day: '',
        contact: '',
        interests: [],
        team: null,
        degree: '',
      },
      newFilter: {
        tag:[],
        gender:"",
        type:"",
      },
      loading: false,
      input: '',
      filter:{
        gender:"",
        type:"",
        tag:[],
        isTrue: false,
      },
      ifOpenPersonDetail: false,
      ifOpenFilter: false,
      filterDialogVisible: false,
    };
  },
  mounted() {
    this.getAllUser();
    this.getAllTag();
  },
  methods: {
    async getAllTag(){
      const apiUrl = 'https://backend.susdorm.online/api/all-interests/';
      try {
        const response = await axios.get(apiUrl,);
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            id: list[i]['id'],
            name: list[i]['name']
          };
        }
        this.all_tag = list;
      } catch (error) {
        this.$message.error(error.toString());
        console.error('Error fetching files:', error);
      }
    },
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
      this.isAbleChat = false;
      this.ifOpenPersonDetail = true;
    },
    openFilter() {
      this.filterDialogVisible = true;
    },
    clearFilterForm() {
      this.resetNewFilter();
      this.newFilter.tag = [];
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
        interests: [],
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
        interests: [],
        team: null,
        degree: '',
      }
    },
    resetNewFilter() {
      this.$refs.newFilterForm.resetFields();
    },
    createNewFilter() {
      this.loading = true;
      //TODO: implement the logic for filtering
      this.filter = {gender: this.newFilter.gender, type:this.newFilter.type, tag:this.newFilter.tag, isTrue: true}
      alert("You select " + this.newFilter.type + ", " + this.newFilter.gender);
      this.closeCreateFilter()
      this.loading = false;
    },
    ifFilter(){

    },
  },
  computed: {
    groupShow() {
      const input = this.input;

      if (input) {
        return this.groups.filter(groups => {
          return (
            (!this.filter.gender || groups.gender === this.filter.gender) &&
            (!this.filter.type || groups.degree === this.filter.type) &&
            (this.filter.tag.length===0 || (groups.interests.length!==0 && groups.interests.some(interest => this.filter.tag.includes(interest))))
          ) && (
            Object.keys(groups).some(key => {
              return String(groups[key]).toLowerCase().indexOf(input.toLowerCase()) > -1;
            })
          );
        });
      }

      return this.groups.filter(groups => {
        return (
          (!this.filter.gender || groups.gender === this.filter.gender) &&
          (!this.filter.type || groups.degree === this.filter.type) &&
          (this.filter.tag.length===0 || (groups.interests.length!==0 && groups.interests.some(interest => this.filter.tag.includes(interest))))
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
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>
<style>
.customDialog {
  background: #F5EFEC;
  width: 70%;
  height: 80%;
  border-radius: 20px;
}
.bot{
  margin-top: 50px;
}
</style>

