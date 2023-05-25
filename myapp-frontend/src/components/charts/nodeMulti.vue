<template >
    <div v-loading.fullscreen.lock="loading" element-loading-background="rgba(13,130,255,0.5)" element-loading-text="LOADING...">
        <h2>{{feature}}</h2>
        <div id="nmDom" class="chart">
    </div>
    </div> 
  </template>
  <script>        
  
  import{onMounted,reactive,inject,onBeforeUnmount,nextTick,ref}from "vue"
  import dataService from '../../services/DataService.js'
  import {mounted, beforeDestroy, chart} from "@/utils/resize"
  import { dataCache,writeData } from "@/utils/storageTools"

  export default {
    props:{
      cluster:String,
      feature:String,
      node_name:ref,
      realTime:{
        type:Boolean,
        default:true
      },
      setDisabled:ref
    },
    setup(props){
        const loading=ref(true)
        let url='node_multi_params?cluster='+props.cluster+'&feature='+props.feature+'&node_name='+props.node_name
        // console.log(url)
        let $echarts=inject("echarts");
  
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
            data=dataCache.value['nodemulti'][props.feature][props.cluster][props.node_name]
            if(data == undefined){
              try{
              data = await dataService.getData(url)
              // console.log(data)
              writeData(data,props.feature,props.cluster,props.node_name)
              // console.log('datacache:',dataCache)
            }catch(error){
              console.error(error)
              return
            }
          }
        }

        function setData() {
            legend=data.data.data.map((v)=>v.mount)
            //console.log(legend)
            timeSource=data.data.time
            //console.log(time)
            let valueArr=data.data.data
            // //console.log(valueArr)
            end=timeSource.length
            for(let iter in valueArr){
                valueDict[valueArr[iter].mount]=valueArr[iter].value 
            }
            
            if(props.realTime==false){
              time=timeSource
              for(let key in valueDict){
                series.push({
                    name:key,
                    type:'line',
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
                    data:valueDict[key].slice(0,interval),
                    showSymbol: false,
                })
              } 
            }
            //console.log(series)
        }

        onMounted(()=>{
          mounted()
          getState().then(() => {
            nextTick(() => {
            props.setDisabled(false)
            //得到注入模块的钩子
            myChart=$echarts.init(document.getElementById("nmDom"),'dark')
            setData()
            loading.value=false
            let options={
              tooltip: {
                trigger: 'axis'
              },
              legend: {
                data: legend
              },
              grid: {
                left: '5%',
                right: '4%',
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
                type: 'value',
                scale:true,
                axisLabel: {
                    formatter: function (value) {
                        var res = value.toString();                                       
                        var numN1 = 0; 
                        var numN2 = 1;
                        var num1=0;
                        var num2=0;
                        var t1 = 1;
                        for(var k=0;k<res.length;k++){
                            if(res[k]==".")
                                t1 = 0;
                            if(t1)
                                num1++;
                            else
                                num2++;                                                                                              
                        }
                                                                        
                        if(Math.abs(value)<1 && res.length>4)
                        {
                            for(var i=2; i<res.length; i++){                                              
                                if(res[i]=="0"){
                                    numN2++;
                                }else if(res[i]==".")
                                    continue;
                                else
                                    break;
                            }
                            var v = parseFloat(value);                                                
                            v = v * Math.pow(10,numN2);
                            return v.toString() + "e-" + numN2;
                        }else if(num1>4)
                        {
                            if(res[0]=="-")
                                numN1 = num1 - 2;
                            else
                                numN1 = num1 - 1;
                            var tmp = parseFloat(value);                                                
                            tmp = tmp / Math.pow(10,numN1);
                            if(num2 > 4)
                                tmp = tmp.toFixed(4);
                            return tmp.toString() + "e" + numN1;
                        }else
                            return parseFloat(value);                                                                                  
                    }
                }
              },
              series: series,
              }
            myChart.setOption(options)
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
      }
      return{
      loading
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
        /* border: 1px,solid blue; */
        margin:.25rem;
        background-color: rgba(13,130,255,0.5);
    }
  </style>