"""
将数据存入数据库中
"""
import pathlib
import re
import sqlite3
import pandas as pd
import os


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


# 构造集群层面的数据库
def db_cluster():
    conn = sqlite3.connect("./database/cluster.db")
    cursor = conn.cursor()
    cursor.execute("create table cluster(date datetime, timestamp timestamp, cluster_name varchar(30), node_name varchar(30), node_ip varchar(30), metric_name varchar(60), value float, primary key(date, cluster_name, metric_name))")
    path = './data'
    files = pathlib.Path(path).glob("*.csv")
    column_header = ['date', 'timestamp', 'cluster_name', 'node_name', 'node_ip', 'metric_name', 'value']
    values = []
    for file in files:
        # 匹配
        pattern = re.compile(r'(.)*==cluster.csv', re.I)
        if re.match(pattern, file.name):
            # print(file.name)
            data, column = read_csv_column(file, ',', 'utf-8')
            for item in data:
                values.clear()
                for column_item in column_header:
                    if column_item in column:
                        values.append(item[column.index(column_item, 0, len(column))])
                    else:
                        values.append('missing')
                # print(values)
                cmd = f"insert into cluster(date, timestamp, cluster_name, node_name, node_ip, metric_name, value) values ('{values[0]}', {values[1]}, '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', {values[6]})"
                cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()


# 构造节点层面单指标数据库
def db_single_node():
    conn = sqlite3.connect("./database/single_node.db")
    cursor = conn.cursor()
    cursor.execute("create table single_node(date datetime, timestamp timestamp, cluster_name varchar(30), node_name varchar(30), node_ip varchar(30), metric_name varchar(60), value float, primary key(date, cluster_name, node_name, node_ip, metric_name))")
    path = './data'
    files = pathlib.Path(path).glob("*.csv")
    for file in files:
        # 匹配
        pattern = re.compile(r'(.)*==node.csv', re.I)
        if re.match(pattern, file.name) and file.name.find('elasticsearch_filesystem_data_available_bytes') == -1:
            print(file.name)
            data, column = read_csv_column(file, ',', 'utf-8')
            for item in data:
                date = item[0]
                timestamp = item[1]
                cluster_name = item[2]
                node_name = item[3]
                node_ip = item[4]
                metric_name = item[5]
                value = item[6]
                cmd = f"insert into single_node(date, timestamp, cluster_name, node_name, node_ip, metric_name, value) values ('{date}', {timestamp}, '{cluster_name}', '{node_name}', '{node_ip}' ,'{metric_name}', {value})"
                cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()


# 构造节点层面多指标数据
def db_multi_node():
    conn = sqlite3.connect("./database/multi_node.db")
    cursor = conn.cursor()
    cursor.execute("create table multi_node(date datetime, timestamp timestamp, cluster_name varchar(30), node_name varchar(30), node_ip varchar(30), mount varchar(30), metric_name varchar(60), value float, primary key(date, cluster_name, node_name, node_ip, mount ,metric_name))")
    path = './data'
    files = pathlib.Path(path).glob("*.csv")
    for file in files:
        # 匹配
        pattern = re.compile(r'(.)*elasticsearch_filesystem_data_available_bytes==node.csv', re.I)
        if re.match(pattern, file.name):
            data, column = read_csv_column(file, ',', 'utf-8')
            for item in data:
                date = item[0]
                timestamp = item[1]
                cluster_name = item[2]
                node_name = item[3]
                node_ip = item[4]
                mount = item[5]
                metric_name = item[6]
                value = item[7]
                cmd = f"insert into multi_node(date, timestamp, cluster_name, node_name, node_ip, mount, metric_name, value) values ('{date}', {timestamp}, '{cluster_name}', '{node_name}', '{node_ip}', '{mount}', '{metric_name}', {value})"
                cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()


def db_volatility():
    conn = sqlite3.connect("./database/volatility.db")
    cursor = conn.cursor()
    cursor.execute("create table volatility(id int, date datetime, timestamp timestamp, value float, primary key(id, date))")
    path = './data'
    files = pathlib.Path(path).glob("*")
    for file in files:
        # 匹配
        pattern = re.compile(r'(\d+).(csv|xlsx)', re.I)
        if re.match(pattern, file.name):
            if str(file.name[-3:]) == "csv":
                id = int(str(file.name[:-4]))
                data, column = read_csv_column(file, ',', 'utf-8')
            else:
                id = int(str(file.name[:-5]))
                data, column = read_xlsx_column(file)
            for item in data:
                date = item[0]
                timestamp = item[1]
                value = item[2]
                cmd = f"insert into volatility(id, date, timestamp, value) values ({id}, '{date}', {timestamp}, {value})"
                cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()


def db_node_name():
    conn = sqlite3.connect("./database/node_name.db")
    cursor = conn.cursor()
    cursor.execute("create table node_name(cluster_name varchar(30), node_name varchar(30), node_ip varchar(30), primary key(cluster_name, node_name, node_ip))")
    path = './data/node_names'
    files = pathlib.Path(path).glob("*")
    for file in files:
        data, column = read_xlsx_column(file)
        cluster_name = str(file.name[:-5])
        for item in data:
            node_name = item[1]
            node_ip = item[0]
            cmd = f"insert into node_name(cluster_name, node_name, node_ip) values ('{cluster_name}', '{node_name}', '{node_ip}')"
            cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    dirs='./database'
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    db_cluster()
    db_single_node()
    db_multi_node()
    db_volatility()
    db_node_name()
