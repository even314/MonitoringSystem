import {ref} from 'vue'

//格式：storage('key')={'time':'inf'}

const key1='history'
const key2='data'
const historyInit={}
const dataInit={
    'cluster':{
    },
    'nodesgl':{
        'elasticsearch_indices_indexing_index_time_seconds_total':{},
        'elasticsearch_indices_search_query_time_seconds':{},
        'elasticsearch_os_load5':{},
        'elasticsearch_process_cpu_percent':{},
        'elasticsearch_transport_rx_size_bytes_total':{},
        'elasticsearch_transport_tx_size_bytes_total':{}
    },
    'nodemulti':{
        'elasticsearch_filesystem_data_available_bytes':{
            'cc-cc408-hya':{},
            'cc-cc553-interestPrice':{}
        }
    }
}

export const historyList=ref(init(key1,historyInit))
export const dataCache=ref(init(key2,dataInit))

/**historyList:{
 "yy-mm-dd1": history1
 "yy-mm-dd2": history2
}**/
export const writeHistory=(inf)=>{
    console.log('inf:',inf)
    var time=currentTime()
    if(historyList.value[time]==undefined)historyList.value[time]=[]
    historyList.value[time]=historyList.value[time].concat(inf)
    console.log('hl:',historyList)
    localStorage.setItem(key1,JSON.stringify(historyList.value))
}

/** type:[cluster,nodesgl,nodemulti]
dataCache: {
    cluster:{
        feather1:
        feather2:
    }
    nodesgl:{
            feather1:{
            cluster1:
            cluster2:
        }
        feather2:
    }
    nodemulti:{
            feature1:{
                cluster1:{
                    node1:
                    node2:
                }
                cluster2:{}
            }
        }
}**/
export const writeData=(inf,feather,cluster_name=null,node_name=null)=>{
    console.log(dataCache.value)
    if(node_name!=null){
        dataCache.value['nodemulti'][feather][cluster_name][node_name]=inf
    }else if(cluster_name!=null){
        dataCache.value['nodesgl'][feather][cluster_name]=inf
    }else{
        dataCache.value['cluster'][feather]=inf
    }
    localStorage.setItem(key2,JSON.stringify(dataCache.value))
    console.log('write data')
}

function del(key,initializer){
    localStorage.removeItem(key)
    localStorage.setItem(key,JSON.stringify(initializer))
}
//删除
export const delHistory=()=>{
    console.log('del his')
    del(key1,historyInit)
    historyList.value=historyInit
}
export const delData=()=>{
    console.log('delData')
    del(key2,dataInit)
    dataCache.value=dataInit
}

function init(key,initializer){
    let historyStore=localStorage.getItem(key)
    // console.log(historyStore)
    if(historyStore==null){
       localStorage.setItem(key,JSON.stringify(initializer))
       return initializer
    }
    //出现错误直接清空
    try {
        var data= JSON.parse(historyStore)
    } catch (error) {
        localStorage.removeItem(key)
        localStorage.setItem(key,JSON.stringify(initializer))
        data=initializer
    }
    return data
}
/**
* 获取当前时间
*/
function currentTime() {
    var date = new Date();
    var year = date.getFullYear(); //月份从0~11，所以加一
    // let month = date.getMonth();
    // console.log("month",month);
    var dateArr = [
        date.getMonth() + 1,
        date.getDate(),
        // date.getHours(),
        // date.getMinutes(),
        // date.getSeconds(), question:把这里注释掉前面就会重写，要么改前端查询方式，要么改write方式
    ];
    //如果格式是MM则需要此步骤，如果是M格式则此循环注释掉
    for (var i = 0; i < dateArr.length; i++) {
        if (dateArr[i] >= 1 && dateArr[i] <= 9) {
            dateArr[i] = "0" + dateArr[i];
        }
    }
    return( year +
        "-" +
        dateArr[0] +
        "-" +
        dateArr[1] )
        // " " +
        // dateArr[2] +
        // ":" +
        // dateArr[3] +
        // ":" +
        // dateArr[4])
}
