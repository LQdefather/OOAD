<template>
  <head>
    <meta name="viewport" content="width=device-width initial-scale=1.0 maximum-scale=1.0 user-scalable=0">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>3D地图</title>
    <style>
      body,html{ margin:0;padding:0;font:12px/16px Verdana,Helvetica,Arial,sans-serif;width: 100%;height: 100%}
      .container{
        height: 100%
      }
    </style>
    <script language="javascript" src="//webapi.amap.com/maps?v=2.0&key=1b23b8fdee7d2a0c193ab87876832a97&plugin=AMap.ControlBar,AMap.ToolBar"></script>
  </head>
</template>

<script setup>
var map


function mapInit(){
  map = new AMap.Map('container', {
    rotateEnable:true,
    pitchEnable:true,
    zoom: 17,
    pitch: 50,
    rotation: -15,
    viewMode:'3D', //开启3D视图,默认为关闭
    zooms:[2,20],
    center:[116.333926,39.997245]
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
}
mapInit()
</script>

<style scoped>

</style>
