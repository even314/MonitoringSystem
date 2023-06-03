import sqlite3

from flask import jsonify,request
from flask import Flask
import pandas as pd
import numpy as np
from numpy import array, zeros, full, argmin, inf, ndim
from math import isinf
from sklearn import preprocessing
import os

app = Flask(__name__)
time_last = 1441

# 导入 CORS
from flask_cors import CORS
# 并允许来自所有域的请求
CORS(app)


def read_csv_column(file, delimiter, encoding):
    data = []
    df = pd.read_csv(file, delimiter, encoding=encoding)
    # 填充缺失值
    df.fillna("missing", inplace=True)
    # 获取列标签
    column_headers = list(df.columns.values)
    for index, row in df.iterrows():
        data.append(row.tolist())
    return data, column_headers


def csv_to_json(file):
    data, column_headers = read_csv_column(file, ',', 'utf-8')
    res = []
    for item in data:
        temp = {}
        for i in range(len(column_headers)):
            temp[column_headers[i]] = item[i]
        res.append(temp)
    return res


def csv_to_json_node(file, node_name):
    data, column_headers = read_csv_column(file, ',', 'utf-8')
    res = []
    for item in data:
        if item[3] == node_name:
            temp = {}
            for i in range(len(column_headers)):
                temp[column_headers[i]] = item[i]
            res.append(temp)
        # if len(res) == 4323:
        #     break
    return res


def read_xlsx_column(file):
    data = []
    df = pd.read_excel(file)
    # 填充缺失值
    df.fillna("missing", inplace=True)
    # 获取列标签
    column_headers = list(df.columns.values)
    for index, row in df.iterrows():
        data.append(row.tolist())
    return data, column_headers


def get_monitoring_data():
    data = []
    time = []
    id = []
    conn = sqlite3.connect("./database/volatility.db")
    cursor = conn.cursor()
    for i in range(20):
        cursor.execute(f"select date,value from volatility where id == {i+1}")
        result = cursor.fetchall()
        temp1 = []
        temp2 = []
        for item in result:
            temp1.append(item[1])
            temp2.append(item[0])
        data.append(temp1)
        time.append(temp2)
        id.append(i + 1)
    cursor.close()
    conn.close()
    return data, time, id


def get_abnormal_data():
    conn = sqlite3.connect("./database/volatility.db")
    cursor = conn.cursor()
    cursor.execute(f"select date,value from volatility where id == 0")
    result = cursor.fetchall()
    data = []
    time = []
    for item in result:
        data.append(item[1])
        time.append(item[0])
    cursor.close()
    conn.close()
    return data, time


def dtw(x, y, dist, warp=1, w=inf, s=1.0):
    """
    计算两个序列的 Dynamic Time Warping（DTW）。
    ：param数组x:N1*M数组
    ：param数组y：N2*M数组
    ：param func dist：用作成本度量的距离
    ：param int warp：计算的偏移量。
    ：param int w：窗口大小，限制匹配项的索引之间的最大距离|i，j|。
    ：param float s：应用于路径的非对角线移动的权重。随着s越来越大，翘曲路径越来越偏向对角线
    返回最小距离、成本矩阵、累计成本矩阵和换行路径。
    """
    assert len(x)
    assert len(y)
    assert isinf(w) or (w >= abs(len(x) - len(y)))
    assert s > 0
    r, c = len(x), len(y)
    if not isinf(w):
        D0 = full((r + 1, c + 1), inf)
        for i in range(1, r + 1):
            D0[i, max(1, i - w):min(c + 1, i + w + 1)] = 0
        D0[0, 0] = 0
    else:
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if (isinf(w) or (max(0, i - w) <= j <= min(c, i + w))):
                D1[i, j] = dist(x[i], y[j])
    C = D1.copy()
    jrange = range(c)
    for i in range(r):
        if not isinf(w):
            jrange = range(max(0, i - w), min(c, i + w + 1))
        for j in jrange:
            min_list = [D0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
            D1[i, j] += min(min_list)
    if len(x) == 1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1], C, D1, path


def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)


# data/cluster
@app.route('/data/cluster', methods=['GET'])
def get_data_cluster():
    # 提取的特征
    feature = request.args.get('feature', default='A')
    cluster_names = ['cc-cc408-hya', 'cc-cc553-interestPrice']
    # 获取时间
    time = []
    conn = sqlite3.connect("./database/cluster.db")
    cursor = conn.cursor()
    cursor.execute(f"select date from cluster where cluster_name == 'cc-cc408-hya' and metric_name == '{feature}'")
    result = cursor.fetchall()
    for item in result:
        time.append(item[0])
    # 依次获取各个集群的数据
    res = []
    for i in range(len(cluster_names)):
        temp = {}
        temp['cluster_name'] = cluster_names[i]
        temp['value'] = []
        cursor.execute(f"select value from cluster where cluster_name == '{cluster_names[i]}' and metric_name == '{feature}'")
        result = cursor.fetchall()
        for item in result:
            temp['value'].append(item[0])
        res.append(temp)

    result = {
        "feature": feature,
        "time": time,
        "data": res
    }

    cursor.close()
    conn.close()

    return jsonify(result)


# data/node_single_param
@app.route('/data/node_single_param', methods=['GET'])
def get_data_single_node():
    # 提取的特征和集群名
    feature = request.args.get('feature', default='A')
    cluster = request.args.get('cluster', default='B')
    # 获取该集群的 node_names 与 对应的 ip 地址
    node_names = []
    node_ips = []
    conn = sqlite3.connect("./database/node_name.db")
    cursor = conn.cursor()
    cursor.execute(f"select node_name,node_ip from node_name where cluster_name == '{cluster}'")
    result = cursor.fetchall()
    for item in result:
        node_names.append(item[0])
        node_ips.append(item[1])
    cursor.close()
    conn.close()
    # 获取时间
    time = []
    conn = sqlite3.connect("./database/single_node.db")
    cursor = conn.cursor()
    cursor.execute(f"select date from single_node where cluster_name == '{cluster}' and node_name == 'data-node-04'  and metric_name == '{feature}'")
    result = cursor.fetchall()
    for item in result:
        time.append(item[0])
    # 依次获取各个集群的数据
    res = []
    for i in range(len(node_names)):
        temp = {}
        temp['node_name'] = f'{node_names[i]}({node_ips[i]})'
        temp['value'] = []
        cursor.execute(f"select value from single_node where cluster_name == '{cluster}' and node_name == '{node_names[i]}' and metric_name == '{feature}'")
        result = cursor.fetchall()
        for item in result:
            temp['value'].append(item[0])
        res.append(temp)

    result = {
        "feature": feature,
        "cluster": cluster,
        "time": time,
        "data": res
    }

    cursor.close()
    conn.close()

    return jsonify(result)


# data/node_multi_params
@app.route('/data/node_multi_params', methods=['GET'])
def get_data_multi_node():
    # 提取的特征和集群名
    feature = request.args.get('feature', default='A')
    cluster = request.args.get('cluster', default='B')
    node_name = request.args.get('node_name', default='C')
    conn = sqlite3.connect("./database/multi_node.db")
    cursor = conn.cursor()
    cursor.execute(f"select distinct mount from multi_node where cluster_name == '{cluster}' and node_name == '{node_name}'")
    result = cursor.fetchall()
    mount_names = []
    # 获取该节点的 mount_names
    for item in result:
        mount_names.append(item[0])
    # 获取时间
    time = []
    cursor.execute(f"select date from multi_node where cluster_name == '{cluster}' and node_name == '{node_name}' and mount == '{mount_names[0]}'")
    result = cursor.fetchall()
    for item in result:
        time.append(item[0])
    # 依次获取各个集群的数据
    res = []
    for mount_name in mount_names:
        temp = {}
        temp['mount'] = mount_name
        temp['value'] = []
        cursor.execute(f"select value from multi_node where cluster_name == '{cluster}' and node_name == '{node_name}' and mount == '{mount_name}'")
        result = cursor.fetchall()
        for item in result:
            temp['value'].append(item[0])
        res.append(temp)

    result = {
        "feature": feature,
        "cluster": cluster,
        "node_name": node_name,
        "time": time,
        "data": res
    }

    cursor.close()
    conn.close()

    return jsonify(result)


# data/node_names
@app.route('/data/node_names', methods=['GET'])
def get_data_node_names():
    cluster_names = ['cc-cc408-hya', 'cc-cc553-interestPrice']
    res = {}
    conn = sqlite3.connect("./database/node_name.db")
    cursor = conn.cursor()
    for cluster in cluster_names:
        cursor.execute(f"select node_name from node_name where cluster_name == '{cluster}'")
        result = cursor.fetchall()
        node_names = []
        for item in result:
            node_names.append(item[0])
        res[cluster] = node_names

    cursor.close()
    conn.close()

    return jsonify(res)


# data/volatility_analysis
@app.route('/data/volatility_analysis', methods=['GET'])
def volatility_analysis(num=5):
    abnormal_data, abnormal_time = get_abnormal_data()
    monitoring_data, monitoring_time, ids = get_monitoring_data()
    distance = []
    abnormal_data_normal = list(preprocessing.maxabs_scale(abnormal_data))
    monitoring_data_normal = []
    for item in monitoring_data:
        monitoring_data_normal.append(list(preprocessing.maxabs_scale(item)))
    # 距离函数
    manhattan_distance = lambda x, y: np.abs(x - y)
    X = np.array(abnormal_data_normal).reshape(-1, 1)
    for i in range(len(ids)):
        Y = np.array(monitoring_data_normal[i]).reshape(-1, 1)
        d, cost_matrix, acc_cost_matrix, path = dtw(X, Y, dist=manhattan_distance)
        distance.append(d)
    dis = sorted(distance)
    res = []
    res_normal = []
    for i in range(num):
        loc = distance.index(dis[i])
        id = ids[loc]
        data = monitoring_data[loc]
        time = monitoring_time[loc]
        temp = {}
        temp['id'] = id
        temp['distance'] = dis[i]
        temp['data'] = data
        temp['time'] = time
        res.append(temp)
        temp_normal = {}
        temp_normal['id'] = id
        temp_normal['distance'] = dis[i]
        temp_normal['data'] = monitoring_data_normal[loc]
        temp_normal['time'] = time
        res_normal.append(temp_normal)

    result = {
        'origin': {
            'source': {
                'time': abnormal_time,
                'value': abnormal_data,
                'errorTime': ['2023/4/23 15:20', '2023/4/23 17:20']
            },
            'result': res
        },
        'normal': {
            'source': {
                'time': abnormal_time,
                'value': abnormal_data_normal,
                'errorTime': ['2023/4/23 15:20', '2023/4/23 17:20']
            },
            'result': res_normal
        }
    }
    return jsonify(result)


# data/node_names
@app.route('/data/warning', methods=['GET'])
def get_data_warning():
    # 提取的特征和集群名
    feature = request.args.get('feature', default='A')
    Max = float(request.args.get('Max', default='1000'))
    Min = float(request.args.get('Min', default='10'))
    files = ['cluster.db', 'multi_node.db', 'single_node.db']
    res = []
    for file in files:
        conn = sqlite3.connect(f'./database/{file}')
        cursor = conn.cursor()
        cursor.execute(f"select distinct metric_name from {file[:-3]}")
        result = cursor.fetchall()
        result = [item[0] for item in result]
        if feature in result:
            cursor.execute(f"select * from {file[:-3]} where metric_name == '{feature}'")
            result = cursor.fetchall()
            for item in result:
                if float(item[-1]) < Min or float(item[-1]) > Max:
                    info=''
                    i=-2
                    j=2
                    while item[i]!=item[j]:
                        info+=item[j]
                        info+='/'
                        j+=1
                    info=info[0:-1]
                    res.append({
                        'time':item[0],
                        'feature':item[-2],
                        'value':str(item[-1]),
                        'info':info
                    })
        cursor.close()
        conn.close()

    resdata = {
        'data': res
    }
    return jsonify(resdata)

@app.route('/data/refresh',methods=['GET'])
def need_to_refresh():
    return jsonify({
        'type':1
    })

if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)