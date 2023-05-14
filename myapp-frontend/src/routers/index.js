
import {createRouter, createWebHistory} from 'vue-router'

import MyHome from '@/views/myHome.vue'

import Clu from '@/components/cluster/clusterItem.vue';

import Nod_Mul from '@/components/node/mulit_metric/multiItem.vue';

import Nod_Sig from '@/components/node/Single_metric/sglItem.vue';

import Error from '@/components/errorPage/error404.vue';

import Compare from '@/components/compare/comView.vue'

import Notice from '@/components/warning/noticeInfo.vue'
import History from '@/components/warning/historyItem.vue'


const router = new createRouter({
    // mode: 'history',
    base: process.env.BASE_URL,
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: '主页面',
            showMenu: true,
            // redirect: '/cluster',
            component:MyHome,
        },
            // children: [
                {
                    path: '/cluster',
                    name: 'cluster',
                    showMenu: true,
                    meta: {
                        icon: 'el-icon-s-grid',
                    },
                    children: [
                        {
                            path: '/cluster/elasticsearch_cluster_health_active_shards',
                            name: 'elasticsearch_cluster_health_active_shards',
                            component: Clu,
                            showMenu: true,
                            meta: {
                                icon: 'el-icon-s-grid',
                            },
                        },
                        {
                            path: '/cluster/elasticsearch_cluster_health_number_of_nodes',
                            name: 'elasticsearch_cluster_health_number_of_nodes',
                            component: Clu,
                            showMenu: true,
                            meta: {
                                icon: 'el-icon-s-grid',
                            },
                        },
                        {
                            path: '/cluster/elasticsearch_cluster_health_status',
                            name: 'elasticsearch_cluster_health_status',
                            component: Clu,
                            showMenu: true,
                            meta: {
                                icon: 'el-icon-s-grid',
                            },
                        },

                    ]
                },
                {
                    path: '/node',
                    name: '节点层面',
                    // component: Patch,
                    showMenu: true,
                    meta: {
                        icon: 'el-icon-remove',
                    },
                    children: [
                        {
                            path: '/node/sig',
                            name: 'nodeSgl',
                            showMenu: true,
                            meta: {
                                icon: 'el-icon-s-marketing',
                            },
                            // component: Nod_Sig_One,
                            children: [
                                {
                                    path: '/node/sig/elasticsearch_indices_indexing_index_time_seconds_total',
                                    name: 'elasticsearch_indices_indexing_index_time_seconds_total',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                                {
                                    path: '/node/sig/elasticsearch_indices_search_query_time_seconds',
                                    name: 'elasticsearch_indices_search_query_time_seconds',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                                {
                                    path: '/node/sig/elasticsearch_os_load5',
                                    name: 'elasticsearch_os_load5',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                                {
                                    path: '/node/sig/elasticsearch_process_cpu_percent',
                                    name: 'elasticsearch_process_cpu_percent',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                                {
                                    path: '/node/sig/elasticsearch_transport_rx_size_bytes_total',
                                    name: 'elasticsearch_transport_rx_size_bytes_total',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                                {
                                    path: '/node/sig/elasticsearch_transport_tx_size_bytes_total',
                                    name: 'elasticsearch_transport_tx_size_bytes_total',
                                    component: Nod_Sig,
                                    showMenu: true,
                                    meta: {
                                        icon: 'el-icon-s-data',
                                    },
                                },
                            ],
                        },
                        {
                            path: '/node/mul',
                            name: 'nodeMul',
                            showMenu: true,
                            meta: {
                                icon: 'el-icon-s-marketing',
                            },
                            // component: Nod_Sig_One,
                            children: [
                                {
                                    path: '/node/mul/elasticsearch_filesystem_data_available_bytes',
                                    name: 'elasticsearch_filesystem_data_available_bytes',
                                    showMenu: true,
                                    component: Nod_Mul,
                                    meta: {
                                        icon: 'el-icon-bell',
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    path: '/warning',
                    name: 'warning',
                    showMenu: true,
                    component: Notice,
                    meta: {
                        icon: 'el-icon-remove',
                    },
                },
                {
                    path: '/compare',
                    name: 'compare',
                    showMenu: true,
                    component: Compare,
                    meta: {
                        icon: 'el-icon-remove',
                    },
                },
                {
                    path: '/history',
                    name: 'historicalWarning',
                    showMenu: true,
                    component: History,
                    meta: {
                        icon: 'el-icon-remove',
                    },
                },
                {
                    path: '/404',
                    name: '404',
                    component:Error,
                },
                {
                    path: '/:pathMatch(.*)',
                    redirect: '/404',
                },
            // ],
        ]
});

export default router;