<template>
  <div class="">
    <label :for="id" class="block text-gray-700 font-bold">{{ label }}</label>
      <label class="block text-gray-700 font-bold">Select a location:</label>
        <SliderCust @option-selected="handleChange" :hierarchical-data="hierarchicalData" :images="optionsTree" @reset-options="resetOptions"/>
    <div v-if="selectedZone && Object.keys(hierarchicalData).length >0 && hierarchicalData[selectedZone]" class="space-y-4 form-select">
      <label for="building" class="block text-gray-700 font-bold">Select a building:</label>
      <el-select v-model="selectedOption2" value-key="id" id="selectOption" placeholder="Select building">
        <el-option
          v-for="option in Object.keys(hierarchicalData[selectedZone])"
          :key="option"
          :value="option"
        />
      </el-select>
    </div>
    <div v-if="selectedZone && selectedOption2 && Object.keys(hierarchicalData).length >0" class="space-y-4 form-select">
      <label for="building" class="block text-gray-700 font-bold">Select a Floor:</label>
      <el-select v-model="selectedOption3" id="selectOption2" value-key="id" placeholder="Select Floor">
        <el-option
          v-for="option in Object.keys(hierarchicalData[selectedZone][selectedOption2])"
          :key="option"
          :value="option"
        />
      </el-select>
    </div>
    <div v-if="selectedZone && selectedOption2 && selectedOption3" class="space-y-4 form-select">
      <label class="block text-gray-700 font-bold">Select a Room:</label>

      <div class="" v-if="selectedOption4 === null">

            <el-row>
            <el-col
              v-for="item in RoomArr"
              :key="item.roomNumber"
              :span="8"

            >
            <el-card @click.native="selectRoom(item)" class="box-card" >
              <img :src="getImageSrc(item.type)" class="list-image" />
              <div class="list-description">
                <h3>{{ item.roomNumber }}</h3>
                <p>{{ handleWord(item.type) }}</p>
              </div>
            </el-card>
            </el-col>
            </el-row>
<!--          </li>-->
<!--        </ul>-->
      </div>
      <div v-else class="el-row">
        <el-col :span="4">
          <p>{{ selectedOption4.roomNumber }}</p>
        </el-col>
        <el-col :span="20" class="right-room">
          <button @click="resetSelection">Change Selection</button>
        </el-col>
      </div>

    </div>

  </div>
</template>


<script>
import data from '@/static/data.json';
import SliderCust from "@/components/SliderCust.vue";
export default {
  components: {SliderCust},

  option1: 0,
  props: {
    id: String, // ID for the dropdown element
    label: String, // Label for the dropdown
    options: Array, // Array of options [{ label: 'Label', value: 'Value' }]
    hierarchicalData: {
      type: Array,
      required: true
    },
  },
  watch: {
    selectedZone: 'emitSelectedOptions',
    selectedOption2: 'emitSelectedOptions',
    selectedOption3: 'emitSelectedOptions',
    selectedOption4: 'emitSelectedOptions',
  },
  data() {

    return {

      optionsTree: data.optionsTree,
      selectedZone: null,
      selectedOption2: null,
      selectedOption3: null,
      selectedOption4: null
    };
  },
  methods: {
    getImageSrc(type) {
      // Add your logic here to determine the image source based on the type
      if (type === 'quadruple_room') {
        return require('@/dist/dorm/dorm1.jpg');
      } else if (type === 'single_room') {
        return require('@/dist/dorm/dorm2.jpg');
      }
    },
    emitSelectedOptions() {
      this.$emit('selected-options', {
        roomId: this.selectedOption4,
      });
    },
    handleWord(word){
      const words = word.split('_');

      // Capitalize each word and join them back with spaces
      return words.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    },
    handleChange(option) {
      this.selectedZone = option;
      console.log('Contents of hierarchicalData:', this.hierarchicalData);
      console.log('Contents of hierarchicalData[selectedZone]:', this.hierarchicalData[this.selectedZone]);
      console.log('Selected Location:', this.selectedZone);
    },
    selectRoom(room) {
      // Set the selectedOption4 when a room is clicked
      console.log("roomNumber: "+ room)
      this.selectedOption4 = room;
    },
    resetSelection: function() {
      this.selectedOption4 = null;
    },
    resetOptions: function(){
      this.selectedZone = null
      this.selectedOption2 = null
      this.selectedOption3 = null
      this.selectedOption4 = null
    }

  },
  computed: {

    //Note: does not validate empty values in each array
    //Note 2: Maybe be appliable to the previous elements
    RoomArr() {
        return this.hierarchicalData[this.selectedZone][this.selectedOption2][this.selectedOption3];
    },
  },
};
</script>

<style>

/* Style form labels */
label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px; /* Add some space below the label */
  margin-top: 8px; /* Add some space below the label */
  color: #333; /* Text color for labels */
}

/* Style input fields */
.form-select {
  width: 100%;
  border-radius: 4px;
  font-size: 16px; /* Font size for input fields */
}

.list-image {
  cursor: pointer;
  width: 100px; /* Adjust image width as needed */
  height: auto; /* Maintain aspect ratio */
  position: relative;
  margin: 20px; /* Adjust spacing between image and description */
}

.list-description {
  flex: 1; /* Allow description to take remaining width */
}

.list-description h3 {
  font-size: 18px; /* Adjust font size */
  margin: 0;
}

.list-description p {
  font-size: 14px; /* Adjust font size */
}

.right-room {
  margin-top: 8px;
  display: flex;
  justify-content: end; /* Align content to the far right */
}

button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 25px; /* Make it more rounded */
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s; /* Add a smooth transition for the button */
}

</style>
