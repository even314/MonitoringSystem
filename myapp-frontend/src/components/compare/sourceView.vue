<template >
        <div id="Dom1" class="chart"/>
</template>
  <script>        
  
  import{onMounted,inject,onBeforeUnmount}from "vue"

  import {mounted, beforeDestroy, chart} from "@/utils/resize"

  export default {
    props:{
        time:[],
        ydata:[],
        errBegin:String,
        errEnd:String
    },
    setup(props){
        // const {data}=toRefs(props)
        // console.log(data)
        let data=props
        console.log(data)

        let $echarts=inject("echarts")
        var myChart=null

        let time = data.time
        let ydata = data.ydata
        let errBegin = data.errBegin
        let errEnd = data.errEnd

        onMounted(()=>{
          mounted()
            
              //得到注入模块的钩子
            myChart=$echarts.init(document.getElementById("Dom1"),'dark')

            let options= {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                type: 'cross'
                }
            },
            toolbox: {
                show: true,
                feature: {
                saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                // prettier-ignore
                data: time
                },
            yAxis: {
                type: 'value',
                axisPointer: {
                snap: true
                }
            },
            series: [
                {
                name: '',
                type: 'line',
                smooth: true,
                // prettier-ignore
                data: ydata,
                markArea: {
                    itemStyle: {
                    color: 'rgba(255, 173, 177, 0.4)'
                    },
                    data: [
                    [
                        {
                        name: 'Error Zone',
                        xAxis: errBegin
                        },
                        {
                        xAxis: errEnd
                        }
                    ],
                    ]
                }
                }
            ],
            }
            myChart.setOption(options)
            chart.value=myChart
                }) 
       onBeforeUnmount(() => {
        beforeDestroy()
        myChart.dispose()
        myChart=null
      })
    }
    }
  </script>
  <style scoped>
    h2{
        height: .6rem;
        color:aliceblue;
        line-height: .6rem;
        text-align: center;
        font-size: .25rem;
    }
    .chart{
        height: 250px;
    }
    .item{
        height: 5.125rem;
        border: 1px,solid blue;
        margin:0;
        background-color: rgba(13,130,255,0.5);
    }
  </style>