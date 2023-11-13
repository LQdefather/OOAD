
<template>
  <AMapTest ref="amapTest" @dorm-selected="handleDormChange" :dorm-selected="handleDormChange"/>
</template>

<style scoped>

</style>

<script>
import PopupWindow from "@/components/PopupWindow.vue";

export default{
  data() {
    return {
      selectedData: {
        DormArea: '',
        DormBuilding: ''
      },

    }
  },
  components: {
    PopupWindow,
  },
  methods: {
    handleDormChange(dormArea, dormBuilding) {
      this.selectedData.DormArea = dormArea;
      this.selectedData.DormBuilding = dormBuilding;
      console.log('Selected Location:', this.selectedData);
    },
    resetDormSelection() {
      // Handle the reset event
      this.selectedData.DormArea = '';
      this.selectedData.DormBuilding = '';
    },

    handleDialogClosed(booleanValue) {
      if(!booleanValue){
        this.resetDormSelection()
      }
    },
  },
  computed: {
    showForm(){
      console.log("Current status:")
      console.log("DormArea "+ this.selectedData.DormArea)
      console.log("DormBuilding "+ this.selectedData.DormBuilding)
      return this.selectedData.DormArea !== '' && this.selectedData.DormBuilding !== '';
    },
  },
}
</script>
