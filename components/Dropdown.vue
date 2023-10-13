<template>
  <div class="">
    <label :for="id" class="block text-gray-700 font-bold">{{ label }}</label>
      <label class="block text-gray-700 font-bold">Select a location:</label>
        <Slider @option-selected="handleChange" :images="optionsTree" @reset-options="resetOptions"/>
    <div v-if="selectedOption" class="space-y-4 form-select">
      <label for="building" class="block text-gray-700 font-bold">Select a building:</label>
      <el-select v-model="selectedOption2" value-key="id" id="selectOption" placeholder="Select building">
        <el-option
          v-for="option in optionsTree[selectedOption-1].Building"
          :key="option.label"
          :label="option.label"
          :value="option.value"
        />
      </el-select>
<!--      <select v-model="selectedOption2" id="selectOption">-->
<!--        <option v-for="option in optionsTree[selectedOption-1].Building" :key="option.label" :value="option.value">{{ option.label }}</option>-->
<!--      </select>-->
    </div>
    <div v-if="selectedOption && selectedOption2" class="space-y-4 form-select">
      <label for="building" class="block text-gray-700 font-bold">Select a Floor:</label>
      <el-select v-model="selectedOption3" id="selectOption2" value-key="id" placeholder="Select Floor">
        <el-option
          v-for="option in optionsTree[selectedOption-1].Building[selectedOption2-1].Floors"
          :key="option.label"
          :label="option.label"
          :value="option.value"
        />
      </el-select>
<!--      <select v-model="selectedOption3" id="selectOption2">-->
<!--        <option-->
<!--          class ="options-style"-->
<!--          v-for="option in optionsTree[selectedOption-1].Building[selectedOption2-1].Floors"-->
<!--          :key="option.label" :value="option.value">{{ option.label }}</option>-->
<!--      </select>-->
    </div>
    <div v-if="selectedOption && selectedOption2 && selectedOption3" class="space-y-4 form-select">
      <label class="block text-gray-700 font-bold">Select a Room:</label>

      <div class="" v-if="selectedOption4 === null">
<!--        <ul class="custom-list" >-->

<!--          <li class="list-item" v-for="item in RoomArr" :key="item.roomNumber" @click="selectRoom(item.roomNumber)">-->
            <el-row>
            <el-col
              v-for="item in RoomArr"
              :key="item.roomNumber"
              :span="8"

            >
            <el-card @click.native="selectRoom(item.roomNumber)" class="box-card" >
              <img :src="item.roomType.image" class="list-image" />
              <div class="list-description">
                <h3>{{ item.roomNumber }}</h3>
                <p>{{ item.roomType.label }}</p>
              </div>
            </el-card>
            </el-col>
            </el-row>
<!--          </li>-->
<!--        </ul>-->
      </div>
      <div v-else class="el-row">
        <el-col :span="4">
          <p>{{ selectedOption4 }}</p>
        </el-col>
        <el-col :span="20" class="right-room">
          <button @click="resetSelection">Change Selection</button>
        </el-col>
      </div>
    </div>

  </div>
</template>


<script>
export default {
  option1: 0,
  props: {
    id: String, // ID for the dropdown element
    label: String, // Label for the dropdown
    options: Array, // Array of options [{ label: 'Label', value: 'Value' }]
  },
  watch: {
    selectedOption: 'emitSelectedOptions',
    selectedOption2: 'emitSelectedOptions',
    selectedOption3: 'emitSelectedOptions',
    selectedOption4: 'emitSelectedOptions',
  },
  data() {

    //During refresh, dummy data route may change to /Dorm/sustech/.... , hence returning 404
    const roomTypes = {
      single: {
        label: 'Single Room',
        image: './dorm/dorm1.jpg',
      },
      double: {
        label: 'Double Room',
        image: './dorm/dorm2.jpg',
      },
      quad: {
        label: 'Suite',
        image: './dorm/dorm3.jpg',
      },
    };

    return {

      optionsTree: [
        {
          label: "Residential College",
          url: "./sustech/lakeside_dorm.jpg",
          value: 1,
          Building: [
            {
              label: "B1",
              value: 1,
              Floors: [
                {
                  label: "F1",
                  value: 1,
                  Room: [
                    {
                      roomNumber: 101,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 102,
                      roomType: roomTypes.double,
                    },
                    {
                      roomNumber: 130,
                      roomType: roomTypes.quad,
                    },
                    {
                      roomNumber: 135,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
                {
                  label: "F2",
                  value: 2,
                  Room: [
                    {
                      roomNumber: 201,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 204,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
              ],
            },
            {
              label: "B2",
              value: 2,
              Floors: [
                {
                  label: "F1",
                  value: 1,
                  Room: [
                    {
                      roomNumber: 101,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 111,
                      roomType: roomTypes.double,
                    },
                    {
                      roomNumber: 112,
                      roomType: roomTypes.double,
                    },
                  ],
                },
                {
                  label: "F2",
                  value: 2,
                  Room: [
                    {
                      roomNumber: 201,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 209,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 212,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
              ],
            },
            {
              label: "B3",
              value: 3,
              Floors: [
                {
                  label: "F1",
                  value: 1,
                  Room: [
                    {
                      roomNumber: 201,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 209,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 212,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
              ],
            },
            {
              label: "B4",
              value: 4,
              Floors: [
                {
                  label: "F1",
                  value: '1',
                  Room: [
                    {
                      roomNumber: 201,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 209,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 212,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
                {
                  label: "F2",
                  value: 2,
                  Room: [
                    {
                      roomNumber: 201,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 209,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 212,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
                {
                  label: "F2",
                  value: 3,
                  Room: [
                    {
                      roomNumber: 212,
                      roomType: roomTypes.quad,
                    },
                  ],
                },
              ],
            },
          ],
        },
        {
          label: "Lychee Hills",
          url: "./sustech/lychee.jpg",
          value: 2,
          Building: [
            {
              label: "B1",
              value: 1,
              Floors: [
                {
                  label: "F1",
                  value: 1,
                  Room: [
                    {
                      roomNumber: 1,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 2,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 3,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 4,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 5,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 6,
                      roomType: roomTypes.single,
                    },
                  ],
                },
                {
                  label: "F2",
                  value: 2,
                  Room: [
                    {
                      roomNumber: 1,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 2,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 3,
                      roomType: roomTypes.single,
                    },
                  ],
                },
              ],
            },
            {
              label: "B2",
              value: 2,
              Floors: [
                {
                  label: "F1",
                  value: 1,
                  Room: [
                    {
                      roomNumber: 1,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 2,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 3,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 4,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 5,
                      roomType: roomTypes.single,
                    },
                    {
                      roomNumber: 6,
                      roomType: roomTypes.single,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],

      selectedOption: null,
      selectedOption2: null,
      selectedOption3: null,
      selectedOption4: null
    };
  },
  methods: {
    emitSelectedOptions() {
      this.$emit('selected-options', {
        selectedOption: this.selectedOption,
        selectedOption2: this.selectedOption2,
        selectedOption3: this.selectedOption3,
        selectedOption4: this.selectedOption4,
      });
    },
    handleChange(option) {
      this.selectedOption = option;
      console.log('Selected Location:', this.selectedOption);
    },
    selectRoom(roomNumber) {
      // Set the selectedOption4 when a room is clicked
      console.log("roomNumber: "+ roomNumber)
      this.selectedOption4 = roomNumber;
    },
    resetSelection: function() {
      this.selectedOption4 = null;
    },
    resetOptions: function(){
      this.selectedOption = null
      this.selectedOption2 = null
      this.selectedOption3 = null
      this.selectedOption4 = null
    }

  },
  computed: {

    //Note: does not validate empty values in each array
    //Note 2: Maybe be appliable to the previous elements
    RoomArr() {
        return this.optionsTree[this.selectedOption - 1].Building[this.selectedOption2 - 1].Floors[this.selectedOption3 - 1].Room;
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
