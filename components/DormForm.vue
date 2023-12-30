
<template>
  <div class="max-w-md bg-gray-100 p-6">
    <transition name="fade">
      <form v-if="showForm" class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md bordered-form" style="align-items: center" :key="uniqueFormKey">
        <h1 style="text-align: center" class="text-2xl font-semibold mb-4">Select Dorm</h1>


        <h2>Collected Dorms by Group</h2>
        <div class="card-grid">
          <div style="" v-if="showCard" v-for="room in bookMarkedRooms">
            <el-card  :class="{ 'selected-card': room.id === selectedRoomInfo.id }" >
              <div @click="handleSelectedOptions(room.id, room)" class="card-content-container">
                <img
                  :src="room.roomLayout"
                  class="image"
                  :alt="require('@/static/dorm/noimage.png')"/>
                <h2>{{ room.zone }}</h2>
                <h2>Building {{room.building}} Floor {{room.floor}}</h2>
                <h2>{{ room.roomNumber }}</h2>
                <h2 style="text-transform: capitalize">{{ removeUnderscore(room.type) }}</h2>
                <p style="text-transform: capitalize">{{room.degree}} Students</p>
              </div>
            </el-card>
          </div>

        </div>
        <!--        <div class="mb-2">-->
        <!--          &lt;!&ndash;Note that selected-options is defined in Dropdown to emit data&ndash;&gt;-->
        <!--          <Dropdown id="dropdown1" :hierarchicalData="hierarchicalData" @selected-options="handleSelectedOptions"/>-->
        <!--        </div>-->
        <div class="selected-option" v-if="selectedOption">
          <el-row>
            <el-col :span="24">
              <p>Selected room : {{selectedRoomInfo.roomNumber}}</p>
            </el-col>
            <el-col :span="24">
              <el-button @click="selectedOption=null">Select Another Room</el-button>
            </el-col>
          </el-row>
          <el-row class="submit-button-row" v-if="selectedOption">
            <el-button @click="submitForm">Submit</el-button>
          </el-row>
          <el-row class="submit-button-row" v-else>
            <el-button disabled>Submit</el-button>
          </el-row>
        </div>


      </form>

    </transition>
    <div v-if="submitted" class="mt-4 text-green-600">
      <p>Form submitted successfully!</p>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import {MessageBox} from "element-ui";

export default {
  name: 'DormForm',
  build: {
    extend(config, { isClient }) {
      // Extend only webpack config for client-bundle
      if (isClient) {
        config.devtool = 'source-map'
      }
    }
  },
  data() {
    return {
      APIFormData: '',
      hierarchicalData: [],
      bookMarkedRooms: [],
      academicPosition: '',
      selectedRoomInfo: {},
      selectedOption: null,
      isSelected: false,
      showCard: true,
      progressNum: 0,
      submitted: false,
      showForm: false,
      uniqueFormKey: "submit-form",
      currentTeam: {}
    };
  },
  watch: {
    academicPosition(newValue, oldValue) {
      // This function will be called whenever myValue changes
      console.log('myValue changed from', oldValue, 'to', newValue);
      this.progressNum = 0
      // You can perform any actions or checks here
    },
  },
  mounted() {
    // Set showForm to true after the component has been mounted
    setTimeout(async () => {

      axios.get('https://backend.susdorm.online/api/bookmark-dorms/', {withCredentials: true})
        .then(response => {
          console.log(response.data)
          response.data.forEach(item => {

            this.bookMarkedRooms.push(item)

          });
          const bookmarkedRoomsArray = Array.from(this.bookMarkedRooms);

          console.log("Bookmarked Rooms");
          console.log(bookmarkedRoomsArray);

        })
        .catch(error => {

          this.error = error.message || 'Error getting book mark dorm';
        });

      this.showForm = true;

    }, 1000);
  },
  methods: {

    handleSelectedOptions(options, room) {

      if(!this.isSelected){
        console.log('Method called')
        this.isSelected = true
        this.selectedOption = options
        this.selectedRoomInfo = room
        console.log('Received selected options:', options);
      }else {

        if(room.id === this.selectedOption){
          this.isSelected = false
          this.selectedOption = null
          this.selectedRoomInfo = {}
        }else {
          this.isSelected = true
          this.selectedOption = options
          this.selectedRoomInfo = room
        }

      }

      // You can do further processing or update the parent component state here
    },
    removeUnderscore(text) {
      // Your custom text transformation logic
      // For example, converting "room_number" to "roomNumber"
      return text.replace(/_/g, ' ');
    },
    submitForm(event) {
      event.preventDefault();

      if(this.selectedOption){

        // Add axios post later....
        axios.post('https://backend.susdorm.online/api/select-dorm/', {
          'id': this.selectedOption
        },{withCredentials:true})
          .then(response => {
            console.log(response.data)
            MessageBox.alert('Successfully submit group on behalf of group！.', 'Alert', {
              confirmButtonText: 'Back',
              type: 'warning'
            });
            this.$router.replace('/DormView');

          })
          .catch(error => {

            console.error('Error:', error.response.data);
            MessageBox.alert('Error storing room: ' + error.response.data.non_field_errors, 'Alert', {
              confirmButtonText: 'Back',
              type: 'warning'
            });
          });

        // Add axios post later....

      }else {
        MessageBox.alert('Havent selected a room yet！.', 'Alert', {
          confirmButtonText: 'Back',
          type: 'warning'
        });
      }

    },
  },
};
</script>

<style scoped>
/* Style the form container */
.max-w-md {
  flex-direction: column;
  max-width: 100%; /* Adjust the maximum width as needed */
  margin: 0 auto;
  padding: 20px;
  background-color: #fff; /* Background color for the form container */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Box shadow for a subtle elevation effect */
  font-family: "Roboto", sans-serif;
}

.bordered-form {
  border: 1px solid #ccc; /* Adjust the border color and width as needed */
}

/* Style form labels */
label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px; /* Add some space below the label */
  color: #333; /* Text color for labels */
}

/* Style input fields */
.form-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc; /* Border for input fields */
  border-radius: 4px;
  font-size: 16px; /* Font size for input fields */
  margin-bottom: 16px; /* Add space below input fields */
}

/* Style the submit button */
button[type="submit"] {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 25px; /* Make it more rounded */
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s; /* Add a smooth transition for the button */
}

.card-grid {
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  justify-content: space-around;
}

.el-card {
  width: 100%;
  margin: 10px;
}

.card-content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.image {
  max-width: 100%;
  max-height: 200px;
}

/* Style the submit button on hover */
button[type="submit"]:hover {
  background-color: #0056b3;
}

/* Style the success message */
.text-green-600 {
  color: #00a700; /* Green color for success message */
  font-weight: bold;
  text-align: center;
  margin-top: 16px; /* Add space above the success message */
}

.submit-button{
  width: 100%;
}

.el-card:hover {
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  background: lightgray;
  transform: scale(1.1); /* Increase scale when the card is selected */
  transition: transform 0.3s; /* Add a transition effect on transform property */
}

.selected-card {
  transform: scale(1.1); /* Increase scale when the card is selected */
  transition: transform 0.3s; /* Add a transition effect on transform property */
}

.selected-option{
   display: flex;
   justify-content: center;
   align-items: center;
   margin-top: 30px; /* Adjust margin for spacing */
   margin-bottom: 10px;
 }

.submit-button-row {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}


</style>

