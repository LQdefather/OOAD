<template>
  <div>
    <choose/>
    <div class="dorm-form-container">
      <DormForm/>
    </div>
    <div>
      <basis />
    </div>
  </div>
</template>

<style>
.dorm-form-container {
  margin-top: 80px; /* 调整上边距以控制位置 */
  padding: 20px;
  margin-bottom: 50px;
}
</style>


<script>
export default {
  name: 'Dorm'
}
</script>
