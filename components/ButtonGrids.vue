<template>
  <div>
  <label class="block text-gray-700 font-bold">Select a location:</label>
  <SliderCust @option-selected="handleLocationChange" :images="options" @reset-options="resetOptions"/>
    <div v-if="selectedID[0]" class="space-y-4 form-select">
      <label for="building" class="block text-gray-700 font-bold">Select a building:</label>
      <el-select v-model="selectedID[1]" value-key="id" id="selectOption" placeholder="Select building">
        <el-option
          v-for="option in this.options[selectedID[0] - 1].Building"
          :key="option.label"
          :label="option.label"
          :value="option.value"
        />
      </el-select>
      <!--      <select v-model="selectedOption2" id="selectOption">-->
      <!--        <option v-for="option in optionsTree[selectedOption-1].Building" :key="option.label" :value="option.value">{{ option.label }}</option>-->
      <!--      </select>-->
    </div>
  <div>
    <ElCarousel v-if="selectedID[1] && selectedID[0]" arrow="always" trigger="click" autoplay="false">
      <ElCarouselItem v-for="floor in this.options[selectedID[0] - 1].Building[selectedID[1]-1].Floors" :key="floor.value">
        <div>{{ floor.label }}</div>
        <div class="button-grid-container">
          <div class="button-grid">
            <button
              v-for="room in getRooms(floor)" :key="room.roomNumber">{{ room.roomNumber }}</button>
          </div>
        </div>
      </ElCarouselItem>
    </ElCarousel>
  </div>
  </div>
</template>

<script>
import data from '@/static/data.json';
import {Carousel} from "element-ui";

export default {
  name: 'ButtonGrids',
  data() {

    return {
      options: data.optionsTree,
      selectedLocation: '',
      selectedID: {
        select1: null,
        select2: null,
        select3: null,
        select4: null
      },
      buttons: ["Button 1", "Button 2", "Button 3","Button 1", "Button 2", "Button 3","Button 1", "Button 2", "Button 3"]
    }
  },
  methods:{
    getRooms(floor) {
      return floor.Room || [];
    },
    handleLocationChange(option) {
      console.log(option)
      this.selectedLocation = this.options[option-1].label;

      // in this case we need to use for selectedID
      this.$set(this.selectedID, 0, option);
    },

    resetOptions: function(){
        this.selectedLocation = '';
        Object.keys(this.selectedID).forEach(key => {
          this.$set(this.selectedID, key, null);
        });
    }
  }
}
</script>

<style scoped>
.button-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); /* Adjust the button size as needed */
  gap: 10px; /* Adjust the gap between buttons as needed */
}
.button-grid-container {
  max-width: 500px; /* Set the maximum width of the container as needed */
  margin: 0 auto; /* Center the container horizontally */
}
button {
  width: 100%;
  padding: 10px;
}
</style>
