<template>
  <div class="map-container">
    <h1 class="title-style">Search Dormitory on This Map!</h1>
  <div class="map-container-wrapper">
    <!-- The container element for the map -->
<!--    <div id="map-container" :style="{ width: mapWidth, height: mapHeight }"></div>-->
    <div v-show="dormArea == null || dormBuilding == null" id="map-container" :style="{ width: mapWidth, height: mapHeight }"></div>
    <!-- Display information when a label is clicked -->
    <div v-if="showRoute">
      <div id="my-panel"/>
      <el-button @click="showRoute=false; initMap()">Cancel</el-button>
    </div>
    <el-dialog  :visible.sync="showBuilding"   :close-on-click-modal="true"
                :close-on-press-escape="true"
                :before-close="handleCloseBuilding">
      <div class="floor-plan-image">
        <div>
        <h1 class="header-style">{{ currentZone + " " +currentBuilding }}</h1>
          <img v-if="currentImage" :src="currentImage" alt="@/static/dorm/noimage.png" style="max-width: 100%; height: auto;">
          <img v-else :src="require('@/static/dorm/noimage.png')" alt="@/static/dorm/noimage.png">
          <h1>{{currentDescription}}</h1>
        </div>
        <el-button v-if="buildingType === 'dormitory'" @click="handleRoute">Details</el-button>
        <el-button @click="showRoute = true; showBuilding = false;initMap()">Show Route</el-button>
      </div>

    </el-dialog>


  </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AMap",
  props :{
    dormArea : String,
    dormBuilding: String,
    newDorm : ['reset-selection'],

  },
  data() {
    return {
      mapWidth: "80%", // Set the initial width of the map container
      mapHeight: "600px", // Set the initial height of the map container
      margin: "0", // Center the map horizontally
      position:"justify",
      newLabelsData: [],
      isLoaded: false,
      showBuilding: false,
      currentBuilding: '',
      currentZone: '',
      currentDescription: '',
      currentImage: null,
      currentCoordinates: null,
      currentUserPosition: null,
      showRoute: false,
      buildingType: null
    };
  },
  mounted() {
    // Initialize the map when the component is mounted
    window._AMapSecurityConfig = {
      securityJsCode:'6dcf279b3051f93ca87a74cf70cca816',
    }

    axios.get('https://backend.susdorm.online/api/builds/',{withCredentials:true})
      .then(response => {
        this.APIFormData = response.data;
        this.APIFormData.forEach(item => {

          // console.log("Received data")
          // console.log(response.data)
          const { id,name,photo,zone, buildingDetails, xlocation,ylocation,type } = item

          var icon = {
            // 图标类型，现阶段只支持 image 类型
            type: 'image',
            // 图片 url
            image: require('@/static/house.png'),
            // 图片尺寸
            size: [64, 64],
            // 图片相对 position 的锚点，默认为 bottom-center
            anchor: 'center',
          };

          if(type==='dormitory'){
            icon = {
              // 图标类型，现阶段只支持 image 类型
              type: 'image',
              // 图片 url
              image: require('@/static/house.png'),
              // 图片尺寸
              size: [64, 64],
              // 图片相对 position 的锚点，默认为 bottom-center
              anchor: 'center',
            };
          } else if(type==='sports'){
            icon = {
              // 图标类型，现阶段只支持 image 类型
              type: 'image',
              // 图片 url
              image: require('@/static/icons/sports.png'),
              // 图片尺寸
              size: [64, 64],
              // 图片相对 position 的锚点，默认为 bottom-center
              anchor: 'center',
            };
          }else if(type==='cafeteria'){
            icon = {
              // 图标类型，现阶段只支持 image 类型
              type: 'image',
              // 图片 url
              image: require('@/static/icons/cafeteria.png'),
              // 图片尺寸
              size: [64, 64],
              // 图片相对 position 的锚点，默认为 bottom-center
              anchor: 'center',
            };
          }else if(type==='library'){
            icon = {
              // 图标类型，现阶段只支持 image 类型
              type: 'image',
              // 图片 url
              image: require('@/static/icons/library.png'),
              // 图片尺寸
              size: [64, 64],
              // 图片相对 position 的锚点，默认为 bottom-center
              anchor: 'center',
            };
          }

          var textStyeLabel = {
            backgroundColor: 'white',
            borderColor: '#fff',
            fontSize: 16,
            fontWeight: 'bold',
            fillColor: 'black',
            strokeWidth: 2,

          };


          const newDataItem = {
            name: zone+ " " + name,
            area: zone,
            building: name, // You can set this to a specific value or extract it from the original data if available
            position: [xlocation, ylocation],
            zooms: [3, 20], // Set the desired zoom values
            opacity: 1, // Set the desired opacity value
            zIndex: 5, // Set the desired zIndex value
            visible: true,
            icon: icon, // Set the desired icon
            photo: photo,
            buildingDetails: buildingDetails,
            type:type,
            text: {
              content: zone+ " " + name + " Building", // Set content to the name
              direction: 'right',
              offset: [-100, 40],
              style: textStyeLabel,
            },
          };


          this.newLabelsData.push(newDataItem);

        });

        this.showForm = true;
        this.initMap();

      })
      .catch(error => {
        this.APIFormData = '';
        this.error = error.message || 'An error occurred';
      });
  },
  methods: {
    loadMap:function() {
      this.isLoaded = true
    },
    handleRoute:function (){
      this.$router.push({ name: 'DormView', params: { zone: this.currentZone, building: this.currentBuilding } });
    },
    handleCloseBuilding:function(){
      this.showBuilding = false
    },
    selectDorm: function(curData){
      this.showBuilding = true
      this.currentZone = curData.area
      this.currentBuilding = curData.building
      this.currentImage = curData.photo
      this.currentDescription = curData.buildingDetails
      this.currentCoordinates = curData.position
      this.buildingType = curData.type
      console.log(curData.area, curData.building)
      // this.$emit('dorm-selected', curData.area, curData.building);

    },
    resetSelection: function() {

      // this.$emit('reset-selection');
    },

    initMap() {
      // Load the AMap API script
          const script = document.createElement('script');

          script.src = '//webapi.amap.com/maps?v=2.0&key=20db94d3028c1d2472ae4f29ab518e4b&plugin=AMap.ControlBar,AMap.ToolBar,AMap.Walking,AMap.Geolocation';
          script.async = true;
          script.onload = () => {
            // Create the map instance
            let map = new AMap.Map('map-container', {
              rotateEnable:true,
              pitchEnable:true,
              zoom: 17,
              pitch: 50,
              rotation: -15,
              viewMode:'3D', //开启3D视图,默认为关闭
              zooms:[2,20],
              center:[113.99913918407441, 22.60212445711336]
            });

            const geolocation = new AMap.Geolocation({
              enableHighAccuracy: true, // 是否使用高精度定位，默认：true
              timeout: 10000, // 设置定位超时时间，默认：无穷大
              offset: [10, 20],  // 定位按钮的停靠位置的偏移量
              zoomToAccuracy: true,  //  定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
              position: 'RB' //  定位按钮的排放位置,  RB表示右下
            })

            geolocation.getCurrentPosition((status, result) => {
              if (status === 'complete') {
                console.log(result);
                this.currentUserPosition = [result.position.KL, result.position.kT];
              } else {
                console.log("Error");
              }
            });


            var controlBar = new AMap.ControlBar({
              position:{
                right:'10px',
                top:'10px'
              }
            });
            controlBar.addTo(map);

            var toolBar = new AMap.ToolBar({
              position:{
                right:'40px',
                top:'110px'
              }
            });
            toolBar.addTo(map);

            if(this.showRoute){
              //获取起终点规划线路
              const driving = new AMap.Walking({
                map: map,
                panel: "my-panel",
              });

              console.log(this.currentUserPosition)
              console.log(this.currentCoordinates)

              driving.search(this.currentUserPosition,this.currentCoordinates, function (status, result) {
                if (status === "complete") {
                  //status：complete 表示查询成功，no_data 为查询无结果，error 代表查询错误
                  //查询成功时，result 即为对应的驾车导航信息
                  console.log(result);
                } else {
                  console.log("获取驾车数据失败：" + result);
                }
              });

            };


            var LabelsData = this.newLabelsData

            // console.log(LabelsData)

            var markers = [];
            var allowCollision = false;
            var layer = new AMap.LabelsLayer({
              zooms: [3, 20],
              zIndex: 1000,
              // collision: false,
              // 设置 allowCollision：true，可以让标注避让用户的标注
              allowCollision,
            });
            // layer.add(markers);
            // 图层添加到地图

            // 初始化 labelMarker
            for (var i = 0; i < LabelsData.length; i++) {

              //must be const!!

              const curData = LabelsData[i];
              // console.log(curData)
              curData.extData = {
                index: i,
              };
              // console.log(curData)

              var labelMarker = new AMap.LabelMarker(curData);
              // 绑定click事件到图标对象上
              labelMarker.on('click', () => {
                // Access the name property from the clicked LabelMarker's data
                this.selectDorm(curData)
                // Print the clicked label's name to the console
              });
              markers.push(labelMarker);
            }
            layer.add(markers);
            map.add(layer);
            // 将 marker 添加到图层

            }


          document.head.appendChild(script);
    },
  },

};
</script>

<style scoped>
.map-container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.map-container{
  background-color: white;
  border: #b3d1c8;
}

.header-style{
  background-color: white;
  text-transform: capitalize;
}

.title-style{
  color: darkgreen;

}

</style>
