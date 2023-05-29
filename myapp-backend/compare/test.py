"""
本脚本主要用于对后端数据处理效率的对比分析
"""

import time
import requests

args1 = {
    "feature": "elasticsearch_cluster_health_active_shards"
}

args2 = {
    "feature": "elasticsearch_indices_indexing_index_time_seconds_total",
    "cluster": "cc-cc408-hya"
}

args3 = {
    "feature": "elasticsearch_filesystem_data_available_bytes",
    "cluster": "cc-cc408-hya",
    "node_name": "data-node-04"
}

args4 = {
    "feature": "elasticsearch_os_load5",
    "MAX": 5,
    "MIN": 4,
}

# cluster node_single_param node_multi_params node_names volatility_analysis warning

print("db")
x = time.time()
response = requests.get('http://127.0.0.1:2020/data/node_single_param', params=args2)
# response = requests.get('http://127.0.0.1:2020/data/volatility_analysis')
data = response.json()
y = time.time()
print(y-x)

print("csv")
x = time.time()
response = requests.get('http://127.0.1.1:2020/data/node_single_param', params=args2)
# response = requests.get('http://127.0.1.1:2020/data/volatility_analysis')
data = response.json()
y = time.time()
print(y-x)
