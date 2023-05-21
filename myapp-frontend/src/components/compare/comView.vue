<template >
    <div v-loading="loading" element-loading-background="rgba(13,130,255,0.5)" element-loading-text="LOADING...">
    <div v-if="visiable1">
        <h2>异常曲线及出现异常的区域</h2>
        <br/>
        <sourceViewVue :time="time" :ydata="ydata" :errBegin="errBegin" :errEnd="errEnd"/>
    </div>
    <h2  v-if="visiable1" style="margin: 1.2rem;">相似波动规律的监控指标曲线集合</h2>
    <div class="item">
        <el-switch  v-if="visiable1" 
        active-color="green"
        inactive-color="red"
        v-model="nomalize"
        active-text="打开归一化比较"
        inactive-text="关闭归一化比较"
        size="large"
        @change="switchChange"
    />
        <div id="Dom" class="chart"></div>
    </div>
    </div>
</template>
<script>        

import{reactive,ref,nextTick,onMounted,inject,onBeforeUnmount}from "vue"
import dataService from '@/services/DataService.js'

import sourceViewVue from "./sourceView.vue"
import {mounted, beforeDestroy, chart_} from "@/utils/resize"

export default {
components:{
    sourceViewVue
},
setup(){
    const loading=ref(true)
    let $echarts=inject("echarts")
    var myChart=null

    const visiable1=ref(false)
    const nomalize=ref(false)
    
    function switchChange(){
        if(myChart!=null){
            if(nomalize.value==false){
                myChart.setOption({
                    series:oriSeries
                })
            }else{
                myChart.setOption({
                    series:norSeries
                })
            }
        }
    }

    const time=ref([1,2])
    const ydata=ref([1,2])
    const errBegin=ref(1)
    const errEnd=ref(2)
    let oriSeries =reactive([])
    let norSeries=reactive([])
    let series=reactive([])
    let legend=reactive([])
    let distance="相似距离：<br/>"

    let url='volatility_analysis'

    let data = reactive({})


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

        time.value=data.data.origin.source.time
        ydata.value=data.data.origin.source.value
        errBegin.value=data.data.origin.source.errorTime[0]
        errEnd.value=data.data.origin.source.errorTime[1]
        
        visiable1.value=true

        oriSeries.push({
            name:'origin',
            type:'line',
            data:ydata.value,
            showSymbol: false,
        })
        norSeries.push({
            name:'origin',
            type:'line',
            data:data.data.normal.source.value,
            showSymbol:false
        })


        legend.push('origin')
        let oriDataset=data.data.origin.result
        let norDataset=data.data.normal.result
        // console.log(data)
        // console.log(dataset)
        for(let iter in oriDataset){
            legend.push(oriDataset[iter].id+"")
            oriSeries.push({
            name:oriDataset[iter].id+"",
            type:'line',
            data:oriDataset[iter].data,
            showSymbol: false,
            })
        }      
        for(let iter in norDataset){
            norSeries.push({
            name:norDataset[iter].id+"",
            type:'line',
            data:norDataset[iter].data,
            showSymbol: false,
        })
        distance=distance+("数据集"+oriDataset[iter].id+": "+oriDataset[iter].distance+'<br/>')
        }
        if(nomalize.value){
            series=norSeries
        }
        else {
            series=oriSeries
        }
    }    

    onMounted(()=>{     
        mounted()
        getState().then(() => {
        nextTick(() => {    
        setData()
        myChart=$echarts.init(document.getElementById("Dom"),'dark')
        loading.value=false 
        myChart.setOption({
        tooltip: {
                // // 表示不使用默认的“显示”“隐藏”触发规则。
                // triggerOn: 'none',
                trigger:'axis',
                formatter: function() {
                return (
                    distance
                )
             }
            },
        legend:{data:legend},
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
            data: time.value,
        },
        yAxis: {
            scale:true,
        },
        series: series,
        })
        chart_.value=myChart
    })}
    )}
    )
    onBeforeUnmount(() => {
        beforeDestroy();
        myChart.dispose()
        myChart=null
        loading.value=true
      })
        return{
            time:time,
            ydata:ydata,
            errBegin:errBegin,
            errEnd:errEnd,
            visiable1,
            nomalize,
            switchChange,
            loading
                }
}

}
</script>
<style scoped>
h2{
    height: .6rem;
    color:aliceblue;
    line-height: .6rem;
    text-align: center;
    font-size: 1.5rem;
    margin-top: 1rem;
}
.chart{
    height: 500px;
}
.item{
    /* height: 5.125rem; */
    background-color: rgba(132, 88, 156, 0.823);
    margin: 0;
    width: 100%;
    /* width: 100%; */
}

</style>