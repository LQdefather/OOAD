<template>
  <div id="app" class="flex-container">
    <div>
      <choose />
    </div>
    <div class="flex-item">
      <selectGroup />
    </div>
    <basis/>
  </div>
</template>

<style>
.group-container {
  margin-top: 80px; /* 调整上边距以控制位置 */
  padding: 20px 20px 0px 0px;
  width: 1400px;
}
</style>


<script>
export default {
  name: "Group"
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

.flex-container {
  display: flex;
  flex-direction: column; /* Stack items vertically */
}

.flex-item {
  margin-bottom: 50px; /* Adjust the spacing between the divs */
}
</style>
