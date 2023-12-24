
<template>
  <div class="max-w-md bg-gray-100 p-6">
    <el-steps :active="progressNum" align-center>
      <el-step title="Select Student Type" />
      <el-step title="Select Zone" />
      <el-step title="Select Building" />
      <el-step title="Select Room" />
    </el-steps>
    <transition name="fade">
      <form v-if="showForm" @submit="submitForm" class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md bordered-form" :key="uniqueFormKey">
        <h2 class="text-2xl font-semibold mb-4">Select Dorm</h2>

        <div class="mb-4">
          <label class="block text-gray-700 font-bold" for="academic-position">
            Select current academic position:
          </label>
          <select v-model="academicPosition" class="form-select w-full p-2 rounded-lg border border-gray-300">
            <option disabled value="">Select type</option>
            <option>Doctorate</option>
            <option>Masters</option>
          </select>
        </div>

        <p class="block text-gray-700 font-bold">Current Room Gender: Male</p>

        <div class="mb-2">
          <!--Note that selected-options is defined in Dropdown to emit data-->
          <Dropdown id="dropdown1" :hierarchicalData="hierarchicalData" @selected-options="handleSelectedOptions"/>
        </div>
        <div class="submit-button">
          <button
            type="submit"
            class="mx-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50"
          >
            Submit
          </button>
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

      academicPosition: '',
      selectedOption: {},

      progressNum: 0,
      devServer: {
        devServer: {
          proxy: {
            '/login': {
              target: 'http://8.138.105.61/api/', // Replace with your Spring server address
              ws: true,
            },
          },
        },
      },
      submitted: false,
      showForm: false,
      uniqueFormKey: "submit-form"
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
    setTimeout(() => {
      axios.get('http://8.138.105.61/api/dorm-room/')
        .then(response => {
          // Handle successful response
          this.APIFormData = response.data;
          this.APIFormData.forEach(item => {
            const { id,zone, building, type, floor, roomNumber } = item;

            if (!this.hierarchicalData[zone]) {
              this.hierarchicalData[zone] = {};
            }
            if (!this.hierarchicalData[zone][building]) {
              this.hierarchicalData[zone][building] = {};
            }

            if (!this.hierarchicalData[zone][building][floor]) {
              this.hierarchicalData[zone][building][floor] = [];
            }

            this.hierarchicalData[zone][building][floor].push({
              id, roomNumber, type
            })
            console.log(this.hierarchicalData)


          });
          console.log(this.hierarchicalData)
          this.error = null;
        })
        .catch(error => {
          // Handle error
          this.APIFormData = '';
          this.error = error.message || 'An error occurred';
        });
      this.showForm = true;
    }, 1000);
  },
  methods: {

    handleSelectedOptions(options) {
      this.selectedOption =options
      // Handle the selected options received from the child component
      console.log('Received selected options:', options);
      // You can do further processing or update the parent component state here
    },
    submitForm(event) {
      event.preventDefault();
      console.log('Form Data:', JSON.stringify(this.formData, null, 2));
      this.showForm = false;
      this.submitted = true;
    },
  },
};
</script>

<style scoped>
/* Style the form container */
.max-w-md {
  flex-direction: column;
  max-width: 750px; /* Adjust the maximum width as needed */
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

.fade-enter-active{
  transition: opacity 1s ease;
}

.fade-enter {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}

</style>

