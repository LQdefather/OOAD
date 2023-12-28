<template>
  <div v-if="dialogVisible">
    <div v-if="loadFinish && hasComments">
    <el-dialog :visible.sync="dialogVisible" :before-close="handleClose">
      <h1 class="header-style">Comment</h1>
      <el-collapse class="">
        <el-collapse-item title="Room Layout" name="1" >
      <img :src="roomImage" :alt="roomImage" class="centered-image">
        </el-collapse-item>
      </el-collapse>
      <div v-for="comment in commentsMap" :key="comment[1].id" class="comment-item " >
<!--        <p>{{comment}}</p>-->
        <el-row>
          <el-col :span="2" >
            <el-avatar :src="comment[1].avatar"/>
          </el-col>
          <el-col :span="17">
            <p class="comment-info"><strong> {{ comment[1].name }}</strong></p>
          </el-col >
          <el-col class="comment-right" :span="5">
            <el-rate v-model="comment[1].rating" size="large" disabled/>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="20">
            <p class="comment-info">{{ comment[1].comment }}</p>
          </el-col>
          <el-col class="comment-right" :span="4">
            <p @click="handleReply(comment[1].id)">{{ (addReply && reply.replyTo === comment[1].id) ? 'Cancel Reply' : 'Reply' }}</p>
          </el-col>
        </el-row>
        <div v-if="addReply && reply.replyTo === comment[1].id" style="display: flex; flex-direction: column; align-items: flex-start;">
          <el-input v-model="reply.comment" placeholder="Please input reply" style="margin-top: 10px;"/>
          <button @click="submitComment(true)" >Submit Reply</button>
        </div>
        <div>
          <div class="replycontainer" v-for="reply in comment[1].replies" :key="comment[1].id">
            <el-row>
              <el-col :span="2">
                <el-avatar :src="reply.avatar"/>
              </el-col>
              <el-col :span="10">
                <p class="comment-info"><strong> {{ reply.name }}</strong></p>
              </el-col >
            </el-row>
            <p>{{ reply.comment }}</p>
          </div>
        </div>
      </div>
      <div style="margin: 10px; border-top: 1px solid #ccc;">
        <button @click="addComment= !addComment" style="background-color: burlywood; margin-top: 20px">{{ addComment ? 'Cancel Comment' : 'Comment' }}</button>
        <div v-if="addComment" >
          <el-rate v-model="comment.rating" size="large" style="margin-top: 10px"/>
          <el-input v-model="comment.comment" placeholder="Type your feeling on this room!" style="margin: 10px;"/>
          <button @click="submitComment(false)" >Submit Comment</button>
        </div>
      </div>
    </el-dialog>

    </div>
  <div v-else>
    <el-dialog title="No Comment" :visible.sync="dialogVisible" :before-close="handleClose">
      <p>No comment</p>
      <div style="margin: 10px; border-top: 1px solid #ccc;">
        <button @click="addComment= !addComment" style="background-color: burlywood; margin-top: 20px">{{ addComment ? 'Cancel Comment' : 'Comment' }}</button>
        <div v-if="addComment" >
          <el-rate v-model="comment.rating" size="large" />
          <el-input v-model="comment.comment" placeholder="Type your feeling on this room!" style="margin: 10px;"/>
          <button @click="submitComment(false)" >Submit Comment</button>
        </div>
      </div>
    </el-dialog>
  </div>
  </div>
</template>

<script>
import axios from "axios"
import {MessageBox} from "element-ui";

export default {
  name: 'CommentSection',
  props: {
    dialogVisible: Boolean,
    roomId: Number, // Specify the type of roomId prop
    roomImage: String
  },
  devServer: {
    https: true
  },
  watch: {
    roomId: function (newVal, oldVal) {
      console.log('Prop changed for selectedRoomId for comment: ', newVal, ' | was: ', oldVal);
      this.getComments(); // Call getComments when roomId changes
    },
  },

  data() {
    return {
      commentsMap: null,
      addComment: false,
      addReply:false,
      loadFinish: false,
      //NOTES: There is no dedicated user logging in, hence we temporarily use user 1 to comment
      comment:{
        user:1,
        comment: null,
        rating: null
      },
      reply:{
        user: 1,
        replyTo: null,
        comment: null
      },
    };
  },
  methods: {
    handleReply(id){

      if(!this.addReply){
        this.addReply = true
        this.reply.replyTo = id

      }else {
        this.addReply = false
        this.reply.comment = null
        this.reply.replyTo = null
      }
    },
    submitComment(isReply){

      let params = {}
      if(isReply){
        params = {
          "dormitory": this.roomId,
          "comment": this.reply.comment,
          "rating": 0,
          "parent": this.reply.replyTo

        }
      }else {
        params = {
          "dormitory": this.roomId,
          "comment": this.comment.comment,
          "rating": this.comment.rating,
          "parent": null
        }
      }

      if((params.comment!=null && params.comment!=='') && params.dormitory!=null ){
        axios.post('https://backend.susdorm.online/api/create-comment/',params,{withCredentials:true}

        ).then(response => {
            this.getComments();
            console.log(response.data);
          })
      }else {
        if(params.comment===null || params.comment===''){
          MessageBox.alert('Please enter a valid comment.', 'Alert', {
            confirmButtonText: 'Back',
            type: 'warning'
          });
        }else {
          MessageBox.alert('System error.', 'Alert', {
            confirmButtonText: 'Back',
            type: 'warning'
          });
        }

      }


    },


    handleClose(){
      console.log(this.commentsMap)
      this.addComment = false
      this.$emit('closeComment', true);
    },
    async getComments() {
      this.loadFinish = false
      const commentsMap = new Map();
      if (this.roomId) {
        const params = {
          dorm_id: this.roomId
        };

        axios.get('https://backend.susdorm.online/api/comment', { params })
          .then(response => {

            const comments = response.data

              comments.forEach(item => {
                const { id, comment, time, avatar, replyTo, name, rating } = item;

                if (!replyTo) {
                  // It is a parent comment
                  commentsMap.set(id, {
                    id, comment, time, name, rating, avatar,
                    replies: []
                  });
                } else {
                  // It is a reply
                  const parentComment = commentsMap.get(replyTo);
                  if (parentComment) {
                    const overallComment = {
                      id, comment, time, name, rating,avatar,
                    };
                    parentComment.replies.push(overallComment);
                  }
                }
              }
              );
              this.commentsMap = commentsMap
              this.loadFinish = true
              console.log(this.commentsMap)

          }
          )
          .catch(error => {
            console.error('An error occurred while fetching comments:', error.message);
          });
      }
    }
  },

  created() {
    // Call getComments when the component is created
    this.getComments();
  },
  computed: {
    hasComments() {
        console.log('Calling coputed function!');
        const hasComments = this.commentsMap.size > 0;
        console.log('Computed value for hasComments:', hasComments);
        console.log("Current Map right now");
        console.log(this.commentsMap);
        return hasComments;
    },
  },
};
</script>

<style scoped>

.container {
  display: flex;
  flex-direction:column;
  align-items: center;
  width: 70%; /* Adjust the width as needed */
  margin: 0 auto; /* Center the container horizontally */
}

.button-grid {
  display: grid;
  grid-template-columns: minmax(100px, 1fr) minmax(100px, 1fr) minmax(100px, 1fr); /* Adjust the button size as needed */
  gap: 10px; /* Adjust the gap between buttons as needed */

//margin-bottom: 40px;
}

.occupied{
  background-color: red;
}

.available{
  background-color: green;
}

ElCarousel {
  height: auto; /* or height: 100%; */
}

.carousel-custom{
  border: 2px solid #b3d1c8;
  margin:0 auto;
  margin-top: 20px;
  height: auto;
  width: 50%;
}

.button-grid-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  height: 100%;
//margin: 0 auto; /* Center the container horizontally */
}
button {
  width: 100%;
  padding: 20px;
}

.comment-item {
  margin-top: 20px;
  text-align: left; /* Align text to the left within the comment-item */
}

.comment-info {
  margin-bottom: 5px; /* Add some spacing between each piece of comment information */
}

.comment-right{
  margin-left: auto;
  margin-right: 0;
  text-align: right;
}

.replycontainer{
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
}

.header-style{
  text-align: center;
}
.centered-image {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  height: auto;
}


</style>
