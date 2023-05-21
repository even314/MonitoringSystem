<template >
    <div v-loading="loading" element-loading-background="rgba(13,130,255,0.5)" element-loading-text="LOADING...">
        <h2>{{feature}}</h2>
        <div id="nsDom" class="chart">
    </div>
    </div> 
  </template>
  <script>        
  
  import{onMounted,reactive,inject,onBeforeUnmount,nextTick,ref}from "vue"
  import dataService from '../../services/DataService.js'
  import {mounted, beforeDestroy, chart} from "../../utils/resize"
  import { dataCache,writeData } from "@/utils/storageTools"

  export default {
    props:{
      cluster:ref,
      feature:String,
      type:{
        type:String,
        default:'value'},
      step:{
        type:String,
        default:''
      },
      realTime:{
        type:Boolean,
        default:false
      },
      setDisabled:ref
    },
    setup(props){
        const loading=ref(true)
        let url='node_single_param?cluster='+props.cluster+'&feature='+props.feature
        // console.log(url)
        let $echarts=inject("echarts");
  
        let data = reactive({})
        let timeSource = reactive([])
        let time=reactive([])
        let series =reactive([])
        let legend=reactive([])
        let selected = reactive({})
        let interval=7
        let valueDict=reactive({})
        var end=0
        var myChart=null
  
        async function getState() {
          data=dataCache.value['nodesgl'][props.feature][props.cluster]
          if(data == undefined){
              try{
              data = await dataService.getData(url)
              // console.log(data)
              writeData(data,props.feature,props.cluster)
              // console.log('datacache:',dataCache)
            }catch(error){
              console.error(error)
              return
            }
          }
        }
        function setData() {
            loading.value=false
            legend=data.data.data.map((v)=>v.node_name)
            for(var i in legend){
              if(i<5)selected[legend[i]]=true;
              else selected[legend[i]]=false;
            }
            timeSource=data.data.time
            end=timeSource.length
            let valueArr=data.data.data

            for(let iter in valueArr){
                valueDict[valueArr[iter].node_name]=valueArr[iter].value 
            }

            if(props.realTime==false){
              time=timeSource
              for(let key in valueDict){
                series.push({
                    name:key,
                    type:'line',
                    step:props.step,
                    data:valueDict[key],
                    showSymbol: false,
                })
              }  
            }else{
              time=timeSource.slice(0,interval)
              for(let key in valueDict){
                series.push({
                    name:key,
                    type:'line',
                    step:props.step,
                    data:valueDict[key].slice(0,interval),
                    showSymbol: false,
                })
              } 
            }
        }

        onMounted(()=>{
          mounted()
          getState().then(() => {
            nextTick(() => {
              props.setDisabled(false)
              setData()
              //得到注入模块的钩子
              myChart=$echarts.init(document.getElementById("nsDom"),'dark')
              
              myChart.setOption({
                tooltip: {
                  trigger: 'axis',
                  hideDelay:100, 
                  transitionDuration:0.4,                      //提示框浮层的移动动画过渡时间，单位是 s,设置为 0 的时候会紧跟着鼠标移动                   //提示框浮层的位置，默认不设置时位置会跟随鼠标的位置,[10, 10],回掉函数，inside鼠标所在图形的内部中心位置，top、left、bottom、right鼠标所在图形上侧，左侧，下侧，右侧，
                },
                legend: {
                  type: 'scroll',
                  orient: 'vertical',
                  right: 10,
                  top: 20,
                  bottom: 20,
                  data: legend,
                  selected:selected
                },
                grid: {
                  left: '5%',
                  right: '20%',
                  bottom: '10%',
                  containLabel: true
                },
                toolbox: {
                  feature: {
                  saveAsImage: {}
                  }
                },
                xAxis: {
                  type: 'category',
                  boundaryGap: false,
                  data: time,
                },
                yAxis: {
                  type: props.type,
                  scale:true,
                },
                series: series,
                })
              if(props.realTime==false){
                myChart.setOption({
                  dataZoom: [
                      {
                        type: "slider",//inside鼠标缩放
                        show: true,
                        start: 0,
                        // end: 10,
                        xAxisIndex: [0],
                      },            
                      {
                        type: "slider",//inside鼠标缩放
                        show: true,
                        start: 0,
                        // end: 10,
                        yAxisIndex: [0],
                        left:"left"
                      }
                  ],
                })
              }else{
                myChart.setOption({
                  animation:false,
                })
              }
              chart.value=myChart
          }) 
        })
      })
       onBeforeUnmount(() => {
        beforeDestroy()
        myChart.dispose()
        myChart=null
        loading.value=true
        props.setDisabled(true)
      })
      var flag=interval
      //实时更新
      if(props.realTime){
        setInterval(function () {
        if(myChart!=null){         
            if(flag>=end){ //重播
            flag=interval
            time=timeSource.slice(0,interval)
            for(let iter in series){
              series[iter].data=valueDict[series[iter].name].slice(0,interval)
            }
          }else{
            time.shift()
            time.push(timeSource[flag])
            for(let iter in series){
              series[iter].data.shift()
              series[iter].data.push(valueDict[series[iter].name][flag])
            }
            flag++
          }
          myChart.setOption({
            xAxis:{
              data:time
            },
            series:series
          })}
    }, 1000)
      return{
      loading
    }
      }
    }
    }
  </script>
  <style scoped>
    h2{
      height: 2rem;
        color:aliceblue;
        line-height: 2rem;
        text-align: center;
        font-size: 1.5rem;
    }
    .chart{
        height: 590px;
    }
    .item{
        height: 5.125rem;
        border: 1px,solid blue;
        margin:.25rem;
        background-color: rgba(13,130,255,0.5);
    }
  </style>