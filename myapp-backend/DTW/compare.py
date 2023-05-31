import random
import sqlite3
import time
from sklearn import preprocessing
from matplotlib import pyplot as plt

from dtw import *


# 性能对比
def comp_work_time():
    total_time = []
    for i in range(10):
        length = (i+1) * 500
        X = []
        for j in range(20):
            temp = []
            for k in range(length):
                temp.append(random.randint(-10, 10))
            X.append(temp)
        Y = []
        for k in range(length):
            Y.append(random.randint(-10, 10))
        functime = []
        print(f"Size of X: {len(X)} x {length}; Length of Y: {length}")
        start_time = time.time()
        ED(X, Y, Euclidean_distance_abs, 3)
        end_time = time.time()
        print(f"Function ED work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        start_time = time.time()
        dtw_origin(X, Y, Euclidean_distance_abs, 3, None)
        end_time = time.time()
        print(f"Function DTW work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        start_time = time.time()
        Ddtw(X, Y, Euclidean_distance_square, 3, None)
        end_time = time.time()
        print(f"Function DDTW work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        start_time = time.time()
        Wdtw(X, Y, 3, None)
        end_time = time.time()
        print(f"Function WDTW work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        start_time = time.time()
        dtw_fast(X, Y, Euclidean_distance_abs, 3, 1, None)
        end_time = time.time()
        print(f"Function FastDTW(radius = 1) work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        start_time = time.time()
        dtw_fast(X, Y, Euclidean_distance_abs, 3, 10, None)
        end_time = time.time()
        print(f"Function FastDTW(radius = 10) work time: {end_time - start_time}")
        functime.append(end_time - start_time)

        # start_time = time.time()
        # dtw_fast(X, Y, Euclidean_distance_abs, 3, 20, None)
        # end_time = time.time()
        # print(f"Function FastDTW(radius = 20) work time: {end_time - start_time}")
        # functime.append(end_time - start_time)

        total_time.append(functime)
    for i in range(len(total_time)):
        print(total_time[i])

def get_monitoring_data():
    data = []
    time = []
    id = []
    conn = sqlite3.connect("../database/volatility.db")
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
    conn = sqlite3.connect("../database/volatility.db")
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


# 效果对比
def comp_performance():
    # 获取目标序列
    Y, time = get_abnormal_data()
    # 获取待检测的序列
    X, time2, id = get_monitoring_data()
    # 将序列数据归一化处理
    Y_normal = list(preprocessing.maxabs_scale(Y))
    X_normal = []
    for item in X:
        X_normal.append(list(preprocessing.maxabs_scale(item)))
    # 保存各个算法执行的结果
    sequence = []
    sequence.append(ED(X_normal, Y_normal, Euclidean_distance_abs, 1)[0][0])
    sequence.append(dtw_origin(X_normal, Y_normal, Euclidean_distance_square, 1, None)[0][0])
    sequence.append(Ddtw(X_normal, Y_normal, Euclidean_distance_square, 1, None)[0][0])
    sequence.append(Wdtw(X_normal, Y_normal, 3, None)[0][0])
    sequence.append(dtw_fast(X_normal, Y_normal, Euclidean_distance_abs, 1, 1, None)[0][0])
    sequence.append(dtw_fast(X_normal, Y_normal, Euclidean_distance_abs, 1, 10, None)[0][0])

    print(Y_normal)

    for i in range(len(sequence)):
        plt.plot([i + 1 for i in range(121)], sequence[i], 'ro-', alpha=0.8, linewidth=1, label='')
        print(sequence[i])
        print('\n\n\n')

    plt.show()


if __name__ == '__main__':
    # comp_work_time()
    comp_performance()