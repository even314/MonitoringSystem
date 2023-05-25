<template>
<el-container class="container">
    <p class="p1">
         请选择您想查询的历史时间: 
    </p>
            <input type="date" v-model="time" />
            <button @click="show">查询</button>
</el-container>
    <el-table :data="history" stripe style="width: 80%" :table-layout="tableLayout" max-height="80vh">
                <el-table-column prop="feature" label="feature" />
                <el-table-column prop="time" label="time" />
                <el-table-column prop="info" label="info" />
                <el-table-column prop="value" label="value"  />
    </el-table>
</template>
<script>
import { historyList} from '@/utils/storageTools';
import { h, ref, reactive} from "vue"
import { ElMessage } from 'element-plus'


export default{
    setup(){
        const time = ref('')
        const history = ref(reactive([]))

        const errmsg = () => {
            ElMessage({
                message: h('p', null,
                h('i', { style: 'color:red' }, '没有查询到有关记录，请重新确认日期！'),
                ),
            })
            history.value=[]
        }
        function show(){
            // console.log(historyList.value)
            if(historyList.value[time.value]!=null){
            history.value=historyList.value[time.value]
            // console.log(history.value)
        }
            else{
                errmsg()
            }
        }
        return{
        show,
        time,
        history,
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
.container{
    height: 4vh;
    position: center;
    margin: 1rem;
}
</style>