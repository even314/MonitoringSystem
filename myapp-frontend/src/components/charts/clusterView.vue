<template >
    <div>
        <h2>{{feature}}</h2>
        <div id="DomClu" class="chart">
    </div>
    </div> 
  </template>
  <script>        
  
  import{onMounted,reactive,inject,onBeforeUnmount,nextTick,ref}from "vue"
  import dataService from '../../services/DataService.js'
  import {mounted, beforeDestroy, chart} from "../../utils/resize"

  export default {
    props:{
      feature:ref,
      type:String,
      step:{
        type:String,
        default:''
      },
      realTime:{
        type:Boolean,
        default:false
      }
    },
    setup(props){
        let url='cluster?feature='+props.feature
        console.log(url)
        let $echarts=inject("echarts")
  
        let data = reactive({})
        let timeSource = reactive([])
        let time=reactive([])
        let series =reactive([])
        let legend=reactive([])
        let interval=10
        let valueDict=reactive({})
        var end=0
        var myChart=null
        
        async function getState() {
            try{
              data = await dataService.getData(url)
              console.log(data)
            }catch(error){
              console.error(error)
              return
            }
        }

        function setData() {
            legend=data.data.data.map((v)=>v.cluster_name)
            // console.log(legend)
            timeSource=data.data.time
            // console.log(time)
            let valueArr=data.data.data
            // console.log(valueArr)
            end=timeSource.length
            for(let iter in valueArr){
                valueDict[valueArr[iter].cluster_name]=valueArr[iter].value 
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
            // console.log(series)
        }

        
        onMounted(()=>{
          // console.log(props.realTime)
          mounted()
          getState().then(() => {
            nextTick(() => {
              setData()
              //得到注入模块的钩子
              myChart=$echarts.init(document.getElementById("DomClu"),'dark')
              
              myChart.setOption({
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  data: legend
                },
                grid: {
                  left: '5%',
                  right: '3%',
                  bottom: '15%',
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
          })
          chart.value=myChart
        }
    }, 1000)
      }
       
      onBeforeUnmount(() => {
        beforeDestroy()
        myChart.dispose()
        myChart=null
      })
    }
    }
  </script>
  <style scoped>
  .btn{
    height: 20px;
    color: aliceblue;
  }
    h2{
        height: 2rem;
        color:aliceblue;
        line-height: 2rem;
        text-align: center;
        font-size: 1.5rem;
    }
    .chart{
        height: 550px;
    }
    .item{
        height: 5.125rem;
        border: 1px,solid blue;
        margin:.25rem;
        background-color: rgba(13,130,255,0.5);
    }
  </style>