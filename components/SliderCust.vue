<template>
  <div class="slider-container" v-if="!selectedOption">
    <button class="prev" @click.prevent="prevSlide">&#10094;</button>
    <transition-group name="fade" tag="div">
      <div :key="currentIndex" @click="selectOption">
        <img :src="currentImg" class="slider-image"  />
        <p class="tag-small">{{ images[currentIndex].label }}</p>
      </div>
    </transition-group>
    <button class="next" @click.prevent="nextSlide">&#10095;</button>
  </div>
  <div v-else class="el-row" >
    <el-col :span="6">
    <p>{{ selectedOption }}</p>
    </el-col>
    <el-col :span="18" class="custom-right">
    <button @click="resetSelection">Change Selection</button>
    </el-col>
  </div>
</template>

<script>
export default {
  name: "SliderCust",
  props: {
    // Define a prop for images
    images: Array,
  },
  data() {
    return {
      timer: null,
      currentIndex: 0,
      selectedOption: null
    };
  },

  mounted: function() {
    this.startSlide();
  },

  methods: {
    startSlide: function() {
      this.timer = setInterval(this.nextSlide, 10000);
    },

    nextSlide: function() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    },

    prevSlide: function() {
      this.currentIndex =
        (this.currentIndex - 1 + this.images.length) % this.images.length;
    },

    selectOption: function() {
      this.selectedOption = this.images[this.currentIndex].label;
      this.$emit('option-selected', this.images[this.currentIndex].value);
      clearInterval(this.timer); // Stop the automatic slide when an option is selected
    },

    resetSelection: function() {
      this.$emit('reset-options');
      this.selectedOption = null;
      this.startSlide(); // Restart the automatic slide when changing the selection
    },


  },

  computed: {
    currentImg: function() {
      return this.images[this.currentIndex].url;
    }
  }
};
</script>

<style scoped>

.custom-right {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end; /* Align content to the far right */
}
/* Styles for the slider-container */
.slider-container {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  min-height: 100px; /* Set a minimum height or adjust as needed */
}

/* Styles for the image container and the image itself */
.image-container {
  flex-grow: 1;
  text-align: center;
}

.slider-image {
  max-width: 100%;
  height: auto;
}

.tag-small {
  position: absolute;
  bottom: 10px; /* Adjust the positioning as needed */
  left: 10px; /* Adjust the positioning as needed */
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 14px;
  border-radius: 4px;
  font-size: 16px;
  margin: 0;
  z-index: 1; /* Ensure the tag is above the image */
}

/* Styles for the Previous and Next buttons */
.prev,
.next {
  cursor: pointer;
  padding: 8px 16px;
  color: white;
  font-weight: bold;
  font-size: 18px;
  transition: 0.7s ease;
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  text-decoration: none;
  user-select: none;
  position: absolute;
  top: 50%; /* Adjust the vertical positioning */
  transform: translateY(-50%);
  z-index: 1; /* Ensure buttons are above the image */
}

.next {
  right: 0;
  border-radius: 0 4px 4px 0;
}

.prev {
  left: 0;
}

.prev:hover,
.next:hover {
  background-color: rgba(0, 0, 0, 0.9);
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

.fade-enter-active{
  transition: opacity 0.5s ease;
  transition-delay: 0.5s; /* Adjust the delay time as needed */
}
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

</style>
