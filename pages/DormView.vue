<!-- App.vue -->
<template>
  <div id="app" class="flex-container">
    <div>
      <choose />
    </div>
    <div class="flex-item">
      <el-row>
          <DormFilter :receivedZone="zone" :receivedBuilding="building"/>
      </el-row>
    </div>
    <div>
      <basis />
    </div>
  </div>
</template>

<script>

export default {
  data(){
    return{
      zone: null,
      building: null
    }

  },
  mounted() {
    console.log("Current params in View Dorm")
    console.log(this.$route.params);
    this.zone = this.$route.params.zone
    this.building = this.$route.params.building
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin-top: 20px;
}

.flex-container {
  display: flex;
  flex-direction: column; /* Stack items vertically */

}

.flex-item {
  margin-bottom: 50px;
  margin-top: 50px;/* Adjust the spacing between the divs */
}
</style>
