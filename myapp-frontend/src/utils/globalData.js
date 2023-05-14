import { reactive } from 'vue';
 
export const globalData = reactive({
  features:{
    cluster:[{
        name:'elasticsearch_cluster_health_active_shards',
        type:'value',
        step:''
    },{
        name:'elasticsearch_cluster_health_number_of_nodes',
        type:'value',
        step:''
    },{
        name:'elasticsearch_cluster_health_status',
        type:'category',
        step:'start'
    }],
    node_single:[{
        name:'elasticsearch_indices_indexing_index_time_seconds_total',
        type:'value',
        step:''
    },{
        name:'elasticsearch_indices_search_query_time_seconds',
        type:'value',
        step:''
    },{
        name:'elasticsearch_os_load5',
        type:'value',
        step:''
    },{
        name:'elasticsearch_process_cpu_percent',
        type:'value',
        step:'start'
    },{
        name:'elasticsearch_transport_rx_size_bytes_total',
        type:'value',
        step:''
    },{
        name:'elasticsearch_transport_tx_size_bytes_total',
        type:'value',
        step:''
    }],
    node_multi:[{   //科学计数法
        name:'elasticsearch_filesystem_data_available_bytes',
        type:'value',
    }]
  },
});