<template>
    <el-container class="container">
            <el-select v-model="nodeSelect" class="mySelect" placeholder="Select" @change="selectChange"
                v-if="isSelectAlive" style="width:max-content">
                <el-option v-for="item in selectArr" :key="item" :label="item.name" :value="item.name" />
            </el-select>
            <p>
               请输入最小值:    
            </p>
            <input type="text" v-model="getValue1" />
            <p>
                请输入最大值:    
            </p>
            <input type="text" v-model="getValue2" />
            <button @click="sub">监测</button>
    </el-container>

        <el-table :data="inform" stripe style="width: 80%" :table-layout="tableLayout" max-height="80vh"
        v-loading.fullscreen.lock="loading" element-loading-background="rgba(13,130,255,0.5)" element-loading-text="LOADING...">
            <el-table-column prop="time" label="time" />
            <el-table-column prop="info" label="info" />
            <el-table-column prop="value" label="value"  />
        </el-table>


</template>

<script>
import dataService from '@/services/DataService.js'
import {ref, reactive } from "vue"
import { historyList, writeHistory} from '@/utils/storageTools';


export default {
    props: {
    },
    components: {
    },
    methods: {
    goTo(path) {
      this.$router.replace(path)
    }
    },
    setup() {

        console.log(historyList.value)


        var feature = ''
        var Min = 0
        var Max = 0
        let url = ''
        // const inform = reactive([])
        const inform = ref(reactive([]))
        const tableLayout=ref('fixed')
        const loading=ref(false)


        var log = reactive([])
        
        function selectChange(data) {
            feature = data
            console.log("feature" + feature)
        }
        const nodeSelect = ref('Select a feature')
        const selectArr = [
            {
                name: 'elasticsearch_cluster_health_active_shards',
            }, {
                name: 'elasticsearch_cluster_health_number_of_nodes',
            }, {
                name: 'elasticsearch_cluster_health_status',
            }, {
                name: 'elasticsearch_indices_indexing_index_time_seconds_total',

            }, {
                name: 'elasticsearch_indices_search_query_time_seconds',

            }, {
                name: 'elasticsearch_os_load5',

            }, {
                name: 'elasticsearch_process_cpu_percent',

            }, {
                name: 'elasticsearch_transport_rx_size_bytes_total',

            }, {
                name: 'elasticsearch_transport_tx_size_bytes_total',

            },
            {
                name: 'elasticsearch_filesystem_data_available_bytes',
            }
        ]
        const isSelectAlive = ref(true)
        const getValue1 = ref(0)
        const getValue2 = ref(1000000)

        function sub() {
            loading.value=true
            Min = getValue1.value
            Max = getValue2.value
            url = 'warning?feature=' + feature + '&Min=' + Min + '&Max=' + Max
            console.log(url)
            getState()
        }
        
        async function getState() {
            if(feature==''){
              loading.value=false
              return 
            }
            try {
                inform.value = (await dataService.getData(url)).data.data
                writeHistory(inform.value)
                console.log(inform.value)
                loading.value=false
            } catch (error) {
                console.error(error)
                loading.value=false
                return
            }
        }

        return {
            nodeSelect,
            // tableData,
            inform,
            isSelectAlive,
            getValue1,
            getValue2,
            selectChange,
            feature,
            Min,
            Max,
            log,
            getState,
            selectArr,
            sub,
            tableLayout,
            loading,
        }
    }
}
</script>

<style>
p{
    color: aliceblue;
    font-size: large;
    font-weight: bold;
    /* text-align: center; */
    margin-top: 0px;
    margin-left: 40px;
    margin-right: 10px;
}
.container{
    height: 4vh;
    position: center;
    margin: 1rem;
}
.mySelect {
    width: 590px;
    margin-left: 280px;
}

.info {
    color: rgb(69, 69, 69);
    background-color: ivory;
}

.text {
    color: aliceblue;
}
/* // 下拉hover上去的背景色 */
.el-select-dropdown .el-select-dropdown__item.hover { 
  background-color: #828282 !important;
  color: aquamarine;
}
.el-select-dropdown .el-select-dropdown__item{
    color: rgb(200, 200, 198);
    font-size: medium;
}
/* 下拉的背景色 */
.el-select-dropdown { 
  background: #022f6a !important;
  border: 1px solid #83929d !important;
  color: chartreuse;
}
 
.mySelect .el-input__inner {
  font-size: 18px !important;
  text-align: center;
/* //   background: rgb(0, 92, 219) !important;
//   border: transparent !important;
//   border-radius: 12px !important; */
  color: #504c4c;
  font-weight: bold;
  cursor: pointer;
  height: 100% !important;
  line-height: 100% !important;
}
 
.mySelect {
  width: 200px;
}
 
.mySelectPopper {
  border: 1px solid #3062ff;
  background-color: #00122a;
}
.mySelectPopper .el-select-dropdown__item.hover {
  background-color: #14265d;
}
.mySelectPopper .el-select-dropdown__item.hover {
  color: #ffffff;
}
.mySelectPopper .el-input__inner {
    color: #ff00dd;
  height: 40px;
  line-height: 40px;
}
.mySelectPopper .el-select-dropdown__item {
  color: #97bffc;
  font-size: 24px !important;
  height: 50px;
  line-height: 50px;
}
.el-select-dropdown {
  background: #2a4e6e !important;
  border: 2px solid #0345eb !important;
}
.mySelectPopper .popper__arrow::after {
  border-bottom-color: #97bffc !important;
}
.mySelectPopper .popper__arrow {
  border-bottom-color: #3062ff !important;
}
 
.el-select
  .el-input
  .el-select__caret.el-input__icon::before {
  content: "\e790" !important;
  color: #f402e0;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
 
.el-select .el-input .el-select__caret {
  transform: rotateZ(0deg) !important;
  color: chartreuse;
}
.el-table{
    text-align: center;
    margin:auto;
}
</style>
