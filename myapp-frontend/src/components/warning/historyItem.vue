<template>
<el-container class="contain">
    <p class="p1">
         请选择您想查询的历史时间: 
    </p>
            <input type="date" v-model="time" />
            <button @click="show">查询</button>
</el-container>
<li v-if="isAlive" v-for="item in history.arr" :key="item.id" class="info">
        {{ item }}
    </li>
</template>
<script>
import { historyList} from '@/utils/storageTools';
import { nextTick, ref, reactive } from "vue"
export default{
    setup(){
        const time = ref(null)
        // let date=""
        const isAlive = ref(false)
        const history = reactive({
            arr: []
        });
        function show(){
            isAlive.value=false
            // date=time.value
            // console.log(typeof(time.value))
            // console.log(time.value)
            // console.log(1)
            // console.log(typeof(time.value)==typeof(temp))
            // console.log(typeof(history.arr))
            // console.log(typeof(history.value[temp].index))
            // console.log(history.arr)
            if(historyList.value[time.value]!=null)
            history.arr=historyList.value[time.value].index
            else{
                history.arr=["没有查询到有关记录，请重新确认日期！"]
            }
            // console.log(2)
            nextTick(() => {
                    isAlive.value = true
                })
                
                console.log(historyList.value[time.value])
        }
        // var temp='2023-05-07'
        // console.log(temp)
        // console.log(typeof(temp))
        // console.log(historyList.value[temp].index)
        // console.log(time.value)
         return{
        show,
        time,
        history,
        isAlive,
        // date,
    }
    },
}
</script>

<style>
.info {
    color: rgb(69, 69, 69);
    background-color: ivory;
}
.p1{
    color: aliceblue;
    font-size: large;
    font-weight: bold;
    margin-left: 500px;
}
.contain{
    height: 30px;
}
</style>