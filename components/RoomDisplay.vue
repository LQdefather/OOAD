<template>
  <div>
    <!-- Iterate over locations -->
    <div v-if="filteredData.length !==0">
      <div v-for="location in Object.keys(this.filteredData)">
        <div class="title-container">
          <el-row >
            <el-col class="title-styles" style="text-align: left" :span="10">
              <h1 class="location-head-style">{{ location }}</h1>
            </el-col>
          </el-row>
        </div>
        <!-- Iterate over buildings in the current location -->
        <div class="building-floor-style">
          <div v-if="filteredData[location]" v-for="building in Object.keys(filteredData[location])" :key="building">
            <div>
              <h2 style="margin-left: 30px;" class="building-header">Building {{ building }}</h2>
              <el-carousel  class="carousel-style" :height="cardHeight" arrow="always" trigger="click">
                <ElCarouselItem  class="carousel-item-style" v-for="floor in Object.keys(filteredData[location][building])" :key="floor">
                  <div class="card-container">
                    <el-row>
                      <el-col :span="22">
                        <h2 class="floor-header">Floor {{ floor }}</h2>
                      </el-col>
                      <el-col class="show-floor-plan" :span="2">
                        <el-button type="info" @click="handleFloorPlan(filteredData[location][building][floor])">View Floor plan</el-button>
                      </el-col>
                    </el-row>
                    <!-- Iterate over rooms in the current floor -->
                    <div id="carId">
                    <el-row  class="room-container">
                      <el-col v-for="(room, index) in filteredData[location][building][floor].rooms" :key="room.id" :span="6">
                        <!-- Start a new row for every 4th element -->
                        <el-row v-if="index % 4 === 0">

                            <el-card :body-style="{ padding: '0px' }" >
                              <div  class="card-content-container">
                                <img v-if="room.interiorImage"
                                  @click="handleComment(room.id, room.roomLayout)"
                                  :src="room.interiorImage"
                                  class="image"
                                  alt="/static/dorm/noimage.png"/>
                                <img v-else
                                  @click="handleComment(room.id, room.roomLayout)"
                                  :src="require('../static/dorm/noimage.png')"
                                  class="image"
                                  alt=""
                                />
                                <h2>{{ room.roomNumber }}</h2>
                                <h2 style="text-transform: capitalize">{{ removeUnderscore(room.type) }}</h2>
                                <p style="text-transform: capitalize">{{room.sex}}: {{room.degree}} Students</p>
                                <p>Stored by: {{room.bookmarkTeamCount}} students</p>
                                <p>Time: {{formattedTime(room.start)}} - {{formattedTime(room.end)}}</p>

                                <p v-if="!isBookmarked(room.id) && !isMultiSelect" @click="collectRoom(room.id)" class="collection-header">收藏</p>
                                <el-checkbox size="large" v-else-if="isMultiSelect" v-model="selectedMultipleRoom[room.id]"></el-checkbox>
                                <p v-else @click="undoCollect(room.id)" class="collection-header">已被收藏</p>
                              </div>
                            </el-card>

                        </el-row>
                        <el-row v-else>
                            <el-card :body-style="{ padding: '0px' }" >
                              <div  class="card-content-container">
                                <img v-if="room.interiorImage"
                                     @click="handleComment(room.id, room.roomLayout)"
                                     :src="room.interiorImage"
                                     class="image"
                                     alt="/static/dorm/noimage.png"/>
                                <img v-else
                                     @click="handleComment(room.id, room.roomLayout)"
                                     :src="require('../static/dorm/noimage.png')"
                                     class="image"
                                     alt=""
                                />
                                <h2>{{ room.roomNumber }}</h2>
                                <h2 style="text-transform: capitalize">{{ removeUnderscore(room.type) }}</h2>
                                <p style="text-transform: capitalize">{{room.degree}} Students</p>
                                <p>Stored by: {{room.bookmarkTeamCount}} students</p>
                                <p>Time: {{formattedTime(room.start)}} - {{formattedTime(room.end)}}</p>
                                <p v-if="!isBookmarked(room.id) && !isMultiSelect" @click="collectRoom(room.id)" class="collection-header">收藏</p>
                                <el-checkbox size="large" v-else-if="isMultiSelect" v-model="selectedMultipleRoom[room.id]"></el-checkbox>
                                <p v-else @click="undoCollect(room.id)" class="collection-header">已被收藏</p>
                              </div>
                            </el-card>
                        </el-row>
                      </el-col>
                    </el-row>

                    </div>
                  </div>
                </ElCarouselItem>
              </el-carousel>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div v-else>
      <p class="desc">No results :(</p>
    </div>
    <div v-if="isMultiSelect" class="submit-button">
    <el-button style="font-size: 30px;padding: 30px; color: white;background-color: #007bff; border-radius: 10px" @click="submitMultipleCollections()" >Submit Collected Rooms</el-button>
    </div>

    <CommentSection  @closeComment="handleReceiveComment" :room-image="this.roomLayout" :dialogVisible="this.showComment" :room-id="this.roomId"/>
    <el-dialog  :visible.sync="showFloorPlan" :close-on-click-modal="true"
                :close-on-press-escape="true"
                :before-close="handleCloseFloorPlan">
      <div v-if="currentFloorPlan" class="floor-plan-image">
        <h1>Floor plan</h1>
        <img :src="currentFloorPlan" alt="@/static/samplefloorplan.png">
      </div>

    </el-dialog>


  </div>
</template>

<script>
import axios from "axios";
import {MessageBox} from "element-ui";
import {max} from "ramda";

export default {
  name: 'RoomDisplay',
  props: {
    filteredData: {
      type: Array,
      required: true,
    },
    isMultiSelect:{
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      data: this.filteredData,
      roomId: null,
      bookMarkedRooms:[],
      roomLayout: null,
      showComment: false,
      showFloorPlan:false,
      showGroups: false,
      displayRoom: true,
      cardHeight: "",
      selectedMultipleRoom:{},
      currentFloorPlan: ''
    };
  },
  mounted(){
    axios.get('https://backend.susdorm.online/api/bookmark-dorms/',{withCredentials:true})
      .then(response => {
        console.log(response.data)
        response.data.forEach(item => {

          const { id,zone, building, type, floor, roomNumber,sex, start, end, degree,roomLayout, floorPlan } = item;
          this.bookMarkedRooms.push(id)

        });
        // const bookmarkedRoomsArray = Array.from(this.bookMarkedRooms);
        //
        //
        // console.log("Bookmarked Rooms");
        // console.log(bookmarkedRoomsArray);

      })
      .catch(error => {

        this.error = error.message || 'Error getting book mark dorm';
      });

    // Weird bug: SetTimeout actually allows us to compute the height
    setTimeout(this.CalculateHeight, 0)

  },
  computed: {
    getMaxCardHeight() {
      return this.cardHeight; // Adjust the default height as needed
    },
  },
  watch: {
    filteredData: function (newVal, oldVal) {
      // Log the changes to the console
      console.log('Prop changed for filtered Data: ', newVal, ' old data was: ', oldVal);
      console.log(newVal)

      // Use the new value in the component
      this.data = newVal;

      // You can perform additional actions with the new value if needed
      // For example, update some internal state or trigger a method
      this.handleDataChange(newVal);
      setTimeout(this.CalculateHeight, 0)

    },
    isMultiSelect: function(newVal, oldVal){

        // if newVal for multiselect is false, delete all collected items
        if(!newVal){
          console.log("Emptying collected multiple rooms")
          this.selectedMultipleRoom = {}
        }
    }
  },
  methods: {
    isBookmarked(roomId){
      return this.bookMarkedRooms.includes(roomId)
    },
    formattedTime(timestamp) {
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    handleFloorPlan(floor){
      this.showFloorPlan = true
      console.log(floor)
      if(floor.floorPlan){
        console.log("Curretn floor Plan selected")
        console.log(floor.floorPlan)
        this.currentFloorPlan = floor.floorPlan

      }else {
        this.currentFloorPlan = ''
      }
    },
    CalculateHeight() {
      const cardElements = document.getElementsByClassName("card-container");
      const cardArray = [...cardElements]; // Convert HTMLCollection to array

      let maxHeight = 0;

      // Loop through each element and find the maximum height
      cardArray.forEach(element => {
        const elementHeight = element.clientHeight;
        console.log("Current height");
        console.log(elementHeight);
        if (elementHeight > maxHeight) {
          maxHeight = elementHeight;
        }
      });

      // Set this.cardHeight to the maximum height + 100px
      this.cardHeight = `${maxHeight + 100}px`;
      console.log(maxHeight);
      console.log(this.cardHeight);
    },
    removeUnderscore(text) {
      // Your custom text transformation logic
      // For example, converting "room_number" to "roomNumber"
      return text.replace(/_/g, ' ');
    },
    undoCollect(id){
      axios.post('https://backend.susdorm.online/api/unbook-dorm/', { id: id }, { withCredentials: true })
        .then(response => {
          // Successful response
          MessageBox.alert('Room successfully uncollected！.', 'Alert', {
            confirmButtonText: 'Back',
            type: 'warning'
          });
          this.bookMarkedRooms = []

          axios.get('https://backend.susdorm.online/api/bookmark-dorms/',{withCredentials:true})
            .then(response => {
              console.log(response.data)
              response.data.forEach(item => {

                const { id,zone, building, type, floor, roomNumber,sex, start, end, degree,roomLayout, floorPlan } = item;
                this.bookMarkedRooms.push(id)

              });
              const bookmarkedRoomsArray = Array.from(this.bookMarkedRooms);

              console.log("Bookmarked Rooms");
              console.log(bookmarkedRoomsArray);
            })
            .catch(error => {

              this.error = error.message || 'Error getting book mark dorm';
            });
        })
        .catch(error => {
          // Error handling
          console.error('Error:', error.response.data);
          // You can also extract more information from the error if needed
          // For example, error.response contains the server response
          MessageBox.alert('Error '+ error.response.data.non_field_errors[0], 'Error', {
            confirmButtonText: 'OK',
            type: 'error'
          });
        });
    },
    handleCloseFloorPlan(done) {
      // Additional logic before closing the dialog (if needed)
      console.log('Closing floor plan dialog.');

      // Set showFloorPlan to false to close the dialog
      this.showFloorPlan = false;

      // Call the done function to close the dialog
      done();
    },
    handleReceiveComment(){
      this.showComment = false
    },
    submitMultipleCollections(){
      if (Object.keys(this.selectedMultipleRoom).length > 0) {
        for (const roomId in this.selectedMultipleRoom) {
          if (this.selectedMultipleRoom[roomId]) {
            console.log(roomId);

            axios.post('https://backend.susdorm.online/api/book-dorm/', { id: roomId }, { withCredentials: true })
              .then(response => {
              })
              .catch(error => {
                // Error handling
                console.error('Error:', error.response.data);
                // You can also extract more information from the error if needed
                // For example, error.response contains the server response
                MessageBox.alert('Error when adding room: '+{ roomId} + ': '+error.response.data.non_field_errors[0], 'Error', {
                  confirmButtonText: 'OK',
                  type: 'error'
                });
              });

            // Add your logic here for each selected room
          }
        }

        this.bookMarkedRooms = []

        axios.get('https://backend.susdorm.online/api/bookmark-dorms/',{withCredentials:true})
          .then(response => {
            // console.log(response.data)
            response.data.forEach(item => {

              const { id,zone, building, type, floor, roomNumber,sex, start, end, degree,roomLayout, floorPlan } = item;
              this.bookMarkedRooms.push(id)

            });
            const bookmarkedRoomsArray = Array.from(this.bookMarkedRooms);

            // console.log("Bookmarked Rooms");
            // console.log(bookmarkedRoomsArray);
          })
          .catch(error => {

            this.error = error.message || 'Error getting book mark dorm';
          });

      } else {
        MessageBox.alert('Error: No rooms selected', 'Error', {
          confirmButtonText: 'OK',
          type: 'error',
        });
      }
    },
    collectRoom(roomID){
      axios.defaults.withCredentials = true
      axios.post('https://backend.susdorm.online/api/book-dorm/', { id: roomID }, { withCredentials: true })
        .then(response => {
          // Successful response
          MessageBox.alert('Room successfully collected to user！.', 'Alert', {
            confirmButtonText: 'Back',
            type: 'warning'
          });

          this.bookMarkedRooms = []

          axios.get('https://backend.susdorm.online/api/bookmark-dorms/',{withCredentials:true})
            .then(response => {
              // console.log(response.data)
              response.data.forEach(item => {

                const { id,zone, building, type, floor, roomNumber,sex, start, end, degree,roomLayout, floorPlan } = item;
                this.bookMarkedRooms.push(id)

              });
              const bookmarkedRoomsArray = Array.from(this.bookMarkedRooms);

              // console.log("Bookmarked Rooms");
              // console.log(bookmarkedRoomsArray);
            })
            .catch(error => {

              this.error = error.message || 'Error getting book mark dorm';
            });
        })
        .catch(error => {
          // Error handling
          console.error('Error:', error.response.data);
          // You can also extract more information from the error if needed
          // For example, error.response contains the server response
          MessageBox.alert('Error '+ error.response.data.non_field_errors[0], 'Error', {
            confirmButtonText: 'OK',
            type: 'error'
          });
        });
    },


    handleComment(roomId,roomImage){
      console.log("selected Room",roomId)
      this.showComment = true,
        this.roomLayout = roomImage
      this.roomId = roomId
    },
    getImageSrc(type) {
      // Add your logic here to determine the image source based on the type
      if (type === 'quadruple_room') {
        return require('../static/dorm/dorm1.jpg');
      } else if (type === 'single_room') {
        return require('../static/dorm/dorm2.jpg');
      }else if(type === 'double_room'){
        return require('../static/dorm/dorm3.jpg');

      }else if(type === 'triple_room'){
        return require('../static/dorm/dorm3.jpg');

      }else {
        return require('../static/dorm/noimage.png');

      }
    },
    handleDataChange(newData) {
      // Do something with the new data
      console.log('Handling data change:', newData);

    },
  },

};
</script>

<style scoped>
.title-container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  /* If 'Helvetica Neue' is not available, fallback to Arial, and then to a generic sans-serif font. */
  font-weight: bold; /* You can adjust the font weight as needed. */
}

.icon-style{
  margin-top: 15px;
  width: 50px;
  height: 50px;
}

.title-styles {
  text-transform: capitalize;
  border-bottom: 2px solid #ccc;
  padding-bottom: 5px;
  font-size: 20px;
  color: white;

  /* Add the gradient background */
  background: linear-gradient(to left, transparent 0%, #1d7304 70%);
  /* Adjust the gradient colors as needed */

  /* Optionally, you can add more styling to enhance the gradient effect */
  overflow: hidden;
}

.image{
  margin-top: 20px;
  height: 200px;
  width: 200px;
}

.el-card{
  height: 100%;
  border: 1px solid #bbbbbb;
}

.el-card:hover {
  cursor: pointer;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
  background: #d2d2d2;
}

.card-content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.location-head-style{
  margin-top: 10px;
  margin-left: 30px;
  margin-bottom: 0;

}

.show-floor-plan{
  text-align: center;
}

.floor-plan-image {
  max-width: 100%; /* Ensure the div doesn't exceed its parent's width */
  position: relative; /* Ensure child elements are positioned relative to this div */
}

.floor-plan-image img {
  width: 100%; /* Make the image fill the width of the container */
  height: auto; /* Maintain the aspect ratio */
  object-fit: cover; /* Cover the entire container while maintaining aspect ratio */
}

.building-floor-style{
  margin-top: 20px;
  margin-bottom: 100px;
  height: 100%;


}

.building-header{
  font-size: 30px; /* You can adjust the color and thickness of the underline */
  display: inline-block; /* Ensure the underline only spans the width of the text */
  color:  #1d7304;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 20px; /* Add some space between the text and the underline */
}

.desc{
  text-align: center;
}

.floor-header{
  font-size: 20px;
  text-align: center;
//display: inline-block; /* Ensure the underline only spans the width of the text */
  margin-bottom: 20px; /* Add some space between the text and the underline */
}

.room-container{
  margin-left: 60px;
  margin-right: 60px;
}

.collection-header{

  text-align: center;
}

.carousel-style{
  margin: 30px 30px;
  border: 2px solid #494949; /* Green color for the border */
  padding: 20px; /* Add padding if needed */
  border-radius: 10px;

}

.carousel-item-style{
  height: 100%;
}

.submit-button{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin-top: 20px; /* Adjust margin as needed */
}


</style>
