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
        <el-row :gutter="10" :justify="'center'" offset="10"  >
          <el-col :span="6" class="grid" v-for="(group,index) in groupShow" :key="index" align="middle">
            <el-card shadow="hover" @click.native="handleGroupCommand(group)"  :id="group.id" style="margin-top: 20px; margin-bottom: 20px">
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
        <el-form-item
          label="Wakeup Time"
          prop="wake"
        >
          <el-select
            v-model="newFilter.wake"
            multiple
            collapse-tags
            style="margin-left: 20px;"
            placeholder="Select Range">
            <el-option
              v-for="item in options_wake"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="Sleep Time"
          prop="sleep"
        >
          <el-select
            v-model="newFilter.sleep"
            multiple
            collapse-tags
            style="margin-left: 20px;"
            placeholder="Select Range">
            <el-option
              v-for="item in options_sleep"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="Select Tags"
          prop="tag"
        >
          <el-checkbox-group v-model="newFilter.tag" size="small" :min="0" :max="5">
            <el-checkbox v-for="(tag,index) in this.all_tag" :label="tag.name" :key="tag">
              {{tag.name.length > 5 ? tag.name.substring(0, 5) + '...': tag.name}}
            </el-checkbox>
          </el-checkbox-group>
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
            type="info"
            @click="openDetail(newGroup.pk)"
          >
            More Detail
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
    <el-dialog
      title="Comments"
      :visible.sync="detailVisible"
      width="50%"
      :before-close="closeDetail">
      <div v-for="comment in comments" :key="comment.id" class="comment-item " >
        <el-row>
          <el-col :span="2" >
            <el-avatar :src="comment.avatar"/>
          </el-col>
          <el-col :span="17">
            <p class="comment-info" v-if="!comment.replyTo"><strong> {{ comment.name }}</strong></p>
            <p class="comment-info" v-if="comment.replyTo"><strong> {{ comment.name }}</strong> _@Anonymous User</p>
          </el-col >
          <el-col class="comment-right" :span="5" v-if="!comment.replyTo">
            <el-rate v-model="comment.rating" size="large" disabled/>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="20">
            <p class="comment-info">{{ comment.comment }}</p>
          </el-col>
        </el-row>
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
      options_wake: [
        {
          value: '0',
          label: 'before 5:00'
        },
        {
          value: '1',
          label: '5:00-7:00'
        },
        {
          value: '2',
          label: '7:00-9:00'
        },
        {
          value: '3',
          label: 'after 9:00'
        },
      ],
      options_sleep: [
        {
          value: '0',
          label: 'before 22:00'
        },
        {
          value: '1',
          label: '22:00-0:00'
        },
        {
          value: '2',
          label: '0:00-2:00'
        },
        {
          value: '3',
          label: 'after 2:00'
        },
      ],
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
        wake: '',
        sleep: '',
        pk: '',
      },
      newFilter: {
        tag:[],
        gender:"",
        type:"",
        wake:[],
        sleep:[],
      },
      loading: false,
      input: '',
      filter:{
        gender:"",
        type:"",
        tag:[],
        isTrue: false,
        wake: [],
        sleep: []
      },
      ifOpenPersonDetail: false,
      ifOpenFilter: false,
      filterDialogVisible: false,
      detailVisible: false,
      comments: [],
      allComments: [],
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
        const response = await axios.get(apiUrl,{ withCredentials: true });
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
        const response = await axios.get(apiUrl,{ withCredentials: true });
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            pk: list[i]['pk'],
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
            wake: list[i]['wake'],
            sleep: list[i]['sleep']
          };
          if ('05:00:00' <= list[i]['wake'] && list[i]['wake'] < '07:00:00') {
            list[i]['wake'] = '1';
          } else if ('07:00:00' <= list[i]['wake'] && list[i]['wake'] < '09:00:00') {
            list[i]['wake'] = '2';
          } else if (list[i]['wake'] >= '09:00:00') {
            list[i]['wake'] = '3';
          } else {
            list[i]['wake'] = '0';
          }
          if ('22:00:00' <= list[i]['sleep'] && list[i]['sleep'] <= '23:59:59') {
            list[i]['sleep'] = '1';
          } else if ('00:00:00' <= list[i]['sleep'] && list[i]['sleep'] < '02:00:00') {
            list[i]['sleep'] = '2';
          } else if (list[i]['sleep'] >= '02:00:00') {
            list[i]['sleep'] = '3';
          } else {
            list[i]['sleep'] = '0';
          }
        }
        this.groups = list;
        // this.$message.success("success");
      } catch (error) {
        this.$message.error(error.toString());
        console.error('Error fetching files:', error);
      }
    },
    async getOneComment(pk){
      const apiUrl = 'https://backend.susdorm.online/api/user-comments/';
      try {
        const dataToSend = {
          pk: pk,
        };
        const response = await axios.post(apiUrl, dataToSend, { withCredentials: true });
        // console.log(response.data);
        let list = response.data;
        for (let i = 0; i < list.length; i++) {
          list[i] = {
            id: list[i]['id'],
            avatar: list[i]['avatar'],
            name: list[i]['name'],
            comment: list[i]['comment'],
            rating: list[i]['rating'],
            time: list[i]['time'],
            replyTo: list[i]['replyTo']
          };
        }
        this.comments = list;
      } catch (error) {
        this.$message.error(pk + error.toString());
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
        wake: group.wake,
        sleep: group.sleep,
        pk: group.pk,
      }
      this.isAbleApply = false;
      this.isAbleChat = false;
      this.ifOpenPersonDetail = true;
    },
    openFilter() {
      this.newFilter = this.filter;
      this.filterDialogVisible = true;
    },
    clearFilterForm() {
      this.resetNewFilter();
    },
    closeFilter(done) {
      this.resetNewFilter();
      done();
    },
    openDetail(pk) {
      this.detailVisible = true;
      this.getOneComment(pk);
    },
    closeDetail(done) {
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
        wake: '',
        sleep: '',
        pk: '',
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
        pk: '',
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
        wake: '',
        sleep: ''
      }
    },
    resetNewFilter() {
      this.$refs.newFilterForm.resetFields();
    },
    createNewFilter() {
      this.loading = true;
      //TODO: implement the logic for filtering
      this.filter = {gender: this.newFilter.gender, type:this.newFilter.type, tag:this.newFilter.tag, wake:this.newFilter.wake, sleep:this.newFilter.sleep, isTrue: true}
      // alert("You select " + this.newFilter.type + ", " + this.newFilter.gender);
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
            (this.filter.tag.length===0 || (groups.interests.length!==0 && groups.interests.some(interest => this.filter.tag.includes(interest)))) &&
            (this.filter.wake.length===0 || this.filter.wake.includes(groups.wake)) &&
            (this.filter.sleep.length===0 || this.filter.sleep.includes(groups.sleep))
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
          (this.filter.tag.length===0 || (groups.interests.length!==0 && groups.interests.some(interest => this.filter.tag.includes(interest)))) &&
          (this.filter.wake.length===0 || this.filter.wake.includes(groups.wake)) &&
          (this.filter.sleep.length===0 || this.filter.sleep.includes(groups.sleep))
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

