<template>
  <div>
    <div class="container">
      <h2>Select a location:</h2>
      <SliderCust @option-selected="handleLocationChange" :images="options" @reset-options="resetOptions"/>
      <div v-if="selectedID[0]" class="form-select">
        <h2>Select a building:</h2>
        <el-select v-model="selectedID[1]" value-key="id" id="selectOption" placeholder="Select building">
          <el-option
            v-for="option in this.options[selectedID[0] - 1].Building"
            :key="option.label"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
      </div>
    </div>
    <div v-if="selectedID[1] && selectedID[0]" class="carousel-custom">
    <ElCarousel height='500px' arrow="always" trigger="click">
      <ElCarouselItem v-for="floor in this.options[selectedID[0] - 1].Building[selectedID[1]-1].Floors" :key="floor.value">
        <h2>{{ floor.label }}</h2>
        <div class="button-grid-container">
          <div class="button-grid">
            <button
              v-for="room in getRooms(floor)"
              :key="room.roomNumber"
              :class="{ 'occupied': room.roomStatus, 'available': !room.roomStatus }"
              @click="handleButton(room.comment)"
            >
              {{ room.roomNumber }}
            </button>
          </div>
        </div>
      </ElCarouselItem>
    </ElCarousel>
    </div>
    <div v-if="filteredComments.length > 0">
      <el-dialog :visible.sync="dialogVisible" :before-close="handleClose">
        <h2>Comment</h2>
        <div v-for="comment in filteredComments" :key="comment.id" class="comment-item">
          <p class="comment-info"><strong> {{ comment.author }}</strong></p>
          <p class="comment-info"><strong>Rating:</strong> {{ comment.rating }}</p>
          <p class="comment-info"><strong>Text:</strong> {{ comment.text }}</p>
          <el-row >
            <el-col :span="11" style="margin: 5px;">
              <button @click="toggleReplies(comment.id)">{{ comment.showreply ? 'Untoggle Replies' : 'Toggle Replies' }}</button>
            </el-col>
            <el-col :span="11" style="margin: 5px;">
              <button @click="addReply(comment.id)" style="background-color: darkgray;;color: white">{{ comment.addreply ? 'Cancel Reply' : 'Reply' }}</button>

            </el-col>
          </el-row>
          <div v-if="comment.addreply" >
            <el-input v-model="newReply" placeholder="Please input" style="margin: 10px;"/>
            <button @click="submitReply(comment.id, comment.newReply)" >Submit Reply</button>
          </div>
          <div v-if="comment.replies.length > 0 && comment.showreply === true">
            <h4>Replies:</h4>
            <ul>
              <li v-for="reply in comment.replies" :key="reply.id">
                {{ reply.text }}
              </li>
            </ul>
          </div>
        </div>
        <div style="margin: 10px; border-top: 1px solid #ccc;">
          <button @click="addComment= !addComment" style="background-color: burlywood; margin-top: 20px">{{ addComment ? 'Cancel Comment' : 'Comment' }}</button>
          <div v-if="addComment" >
            <el-rate v-model="addCommentContent.ratings" size="large" style="margin-top: 10px"/>
            <el-input v-model="newComment" placeholder="Type your feeling on this room!" style="margin: 10px;"/>
            <button @click="handleComment" >Submit Comment</button>
          </div>
        </div>
      </el-dialog>
    </div>
    <div v-if="filteredComments.length < 1 && isSelectedButton === true">
      <el-dialog title="No Comment" :visible.sync="dialogVisible" :before-close="handleClose">
        <p>No comment</p>
        <div style="margin: 10px; border-top: 1px solid #ccc;">
          <button @click="addComment= !addComment" style="background-color: burlywood; margin-top: 20px">{{ addComment ? 'Cancel Comment' : 'Comment' }}</button>
          <div v-if="addComment" >
            <el-rate v-model="addCommentContent.ratings" size="large" />
            <el-input v-model="addCommentContent.comment" placeholder="Type your feeling on this room!" style="margin: 10px;"/>
            <button @click="handleComment" >Submit Comment</button>
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import data from '@/static/data.json';
import {ref} from "vue";

export default {
  name: 'ButtonGrids',
  data() {

    return {
      options: data.optionsTree,
      comments: data.comments,
      rooms: [],
      dialogVisible: true,
      roomCommentArr: [],
      selectedLocation: '',
      isSelectedButton: false,
      addComment: false,
      submitReply: false,
      newReply:"",
      roomNumber: 0,
      selectedID: {
        select1: null,
        select2: null,
        select3: null,
        select4: null
      },
      addCommentContent:{
        ratings: 0,
        comment:""
      },
    }
  },
  computed: {
    filteredComments() {
      // Filter comments based on the roomIds array
      // console.log("Comment Array: ",this.roomCommentArr)
      if(this.comments!==[] && this.roomCommentArr!== null){
        return this.comments.filter(comment => this.roomCommentArr.includes(comment.id));
      }else {
        return []
      }
    },

  },
  methods:{
    getRooms(floor) {
      this.rooms = floor.Room || []
      return floor.Room || [];
    },
    handleLocationChange(option) {
      // console.log(option)
      this.selectedLocation = this.options[option-1].label;

      // in this case we need to use for selectedID
      this.$set(this.selectedID, 0, option);
    },
    handleButton(commentArr){
      this.isSelectedButton = true
      if (commentArr){
        this.roomCommentArr = commentArr

      }else {
        this.roomCommentArr = []
      }
    },
    carouselHeight() {
      console.log("current Rooms: ", this.rooms);
      return this.rooms.length * 50 // Adjust the multiplier as needed
    },

    handleComment(){
      alert("Comment submitted!");
    },
    handleClose(){
      this.roomCommentArr = []
      this.isSelectedButton = false
      this.addComment = false
    },
    resetOptions: function(){
        this.selectedLocation = '';
        Object.keys(this.selectedID).forEach(key => {
          this.$set(this.selectedID, key, null);
        });
    },
    toggleReplies(commentID){
      this.comments[commentID-1].showreply = !this.comments[commentID-1].showreply
    },
    addReply(commentID){
      this.comments[commentID-1].addreply = !this.comments[commentID-1].addreply

    }
  }
}
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
  text-align: left; /* Align text to the left within the comment-item */
}

.comment-info {
  margin-bottom: 5px; /* Add some spacing between each piece of comment information */
}

</style>
