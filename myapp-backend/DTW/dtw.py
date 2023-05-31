from collections import defaultdict


def ED(x, y, dist, k):
    """
        @param x 序列1，可以是数据或是矩阵
        @param y 序列2，待匹配的目标序列
        @param dist 自定义距离计算方法，这里选择欧氏距离
        @param k 返回与目标序列相似度最高的 K 条序列
    """
    m = len(x)
    len_y = len(y)
    dis = []
    # 依次计算各条输入序列与目标序列的相似度
    for i in range(m):
        len_x = len(x[i])
        sum = 0
        for j in range(min(len_x, len_y)):
            sum += dist(x[i][j], y[j])
        dis.append(sum)
    sort_dis = sorted(dis)
    top_K = []
    for i in range(k):
        top_K.append(x[dis.index(sort_dis[i])])
    return top_K, sort_dis[0:k]


def dtw_origin(x, y, dist, k, window=None):
    """
    @param x 序列1，可以是数据或是矩阵
    @param y 序列2，待匹配的目标序列
    @param window 序列设置要走的范围，默认为None会将矩阵遍历一遍
    @param dist 自定义距离计算方法，可以是欧氏距离，汉明距离等等
    @param k 返回与目标序列相似度最高的 K 条序列
    """
    m = len(x)
    len_y = len(y)
    dis = []
    for l in range(m):
        len_x = len(x[l])
        x_row = x[l]
        if window is None:
            window = [(i, j) for i in range(len_x) for j in range(len_y)]
        window = ((i + 1, j + 1) for i, j in window)
        # 初始化矩阵中的其他元素为 inf 和 D[0, 0]=0；D使用元组记录矩阵的值
        D = defaultdict(lambda: (float('inf'),))
        D[0, 0] = (0, 0, 0)
        # 按照公式进行规划计算
        for i, j in window:
            dt = dist(x_row[i - 1], y[j - 1])
            D[i, j] = min((D[i - 1, j][0] + dt, i - 1, j), (D[i, j - 1][0] + dt, i, j - 1),
                          (D[i - 1, j - 1][0] + dt, i - 1, j - 1), key=lambda a: a[0])
        dis.append(D[len_x, len_y][0])
    sort_dis = sorted(dis)
    top_K = []
    for i in range(k):
        top_K.append(x[dis.index(sort_dis[i])])
    return top_K, sort_dis[0:k]


def dtw(x, y, dist, window=None):
    """
    @param x 序列1，可以是向量，矩阵，不局限于一个数列，但是dist要匹配
    @param y 序列2，可以是向量，矩阵，不局限于一个数列，但是dist要匹配
    @param window 序列设置要走的范围，当使用Sakoe-Chiba Bands就需要自定义缩小的范围，这里默认None会矩阵全走一遍
    @param dist 自定义距离计算方法，可以是欧氏距离，汉明距离等等
    """
    len_x, len_y = len(x), len(y)
    if window is None:
        window = [(i, j) for i in range(len_x) for j in range(len_y)]
    # 相当于矩阵的索引 i=1,2,...len_x+1 j=1,2,...len_y+1
    window = ((i + 1, j + 1) for i, j in window)

    # 初始化矩阵中的其他元素inf和D[0, 0]=0；D使用元组记录矩阵的值和path的i,j
    D = defaultdict(lambda: (float('inf'),))
    D[0, 0] = (0, 0, 0)

    # 按照公式进行规划计算
    for i, j in window:
        dt = dist(x[i - 1], y[j - 1])
        D[i, j] = min((D[i - 1, j][0] + dt, i - 1, j), (D[i, j - 1][0] + dt, i, j - 1),
                      (D[i - 1, j - 1][0] + dt, i - 1, j - 1), key=lambda a: a[0])

    # 求解路径
    path = []
    i, j = len_x, len_y
    while not (i == j == 0):
        path.append((i - 1, j - 1))
        i, j = D[i, j][1], D[i, j][2]
    path.reverse()
    return (D[len_x, len_y][0], path)


def reduce_by_half(x):
    """
    分辨率减半，使用平均的方法
    """
    return [(x[i] + x[1 + i]) / 2 for i in range(0, len(x) - len(x) % 2, 2)]


def expand_window(path, len_x, len_y, radius):
    """
    计算radius下的时间窗
    """
    path_ = set(path)
    for i, j in path:
        for a, b in ((i + a, j + b)
                     for a in range(-radius, radius + 1)
                     for b in range(-radius, radius + 1)):
            path_.add((a, b))

    window_ = set()
    for i, j in path_:
        for a, b in ((i * 2, j * 2), (i * 2, j * 2 + 1),
                     (i * 2 + 1, j * 2), (i * 2 + 1, j * 2 + 1)):
            window_.add((a, b))

    window = []
    start_j = 0
    for i in range(0, len_x):
        new_start_j = None
        for j in range(start_j, len_y):
            if (i, j) in window_:
                window.append((i, j))
                if new_start_j is None:
                    new_start_j = j
            elif new_start_j is not None:
                break
        start_j = new_start_j
    return window


def fastdtw(x, y, radius, dist):
    min_time_size = radius + 2

    # 长度小于min_time_size，直接使用DTW计算
    if len(x) < min_time_size or len(y) < min_time_size:
        return dtw(x, y, dist=dist)

    # 每次粗化一半，得到新的序列
    x_shrinked = reduce_by_half(x)
    y_shrinked = reduce_by_half(y)

    # 递归计算，直到满足len(x) < min_time_size or len(y) < min_time_size则回溯
    distance, path = fastdtw(x_shrinked, y_shrinked, radius=radius, dist=dist)

    # 根据radius计算新的计算范围
    window = expand_window(path, len(x), len(y), radius)
    return dtw(x, y, dist=dist, window=window)


def dtw_fast(x, y, dist, k, radius, window=None):
    """
        @param x 序列1，可以是数据或是矩阵
        @param y 序列2，待匹配的目标序列
        @param window 序列设置要走的范围，默认为None会将矩阵遍历一遍
        @param dist 自定义距离计算方法，可以是欧氏距离，汉明距离等等
        @param k 返回与目标序列相似度最高的 K 条序列
        @param radius 半径参数
    """
    m = len(x)
    len_y = len(y)
    dis = []
    for i in range(m):
        len_x = len(x[i])
        distance, path = fastdtw(x[i], y, radius, dist)
        dis.append(distance)
    sort_dis = sorted(dis)
    top_K = []
    for i in range(k):
        top_K.append(x[dis.index(sort_dis[i])])
    return top_K, sort_dis[0:k]


# Derivative Dynamic Time Warping
def Ddtw(x, y, dist, k, window=None):
    """
        @param x 序列1，可以是数据或是矩阵
        @param y 序列2，待匹配的目标序列
        @param window 序列设置要走的范围，默认为None会将矩阵遍历一遍
        @param dist 自定义距离计算方法，可以是欧氏距离，汉明距离等等
        @param k 返回与目标序列相似度最高的 K 条序列
    """
    m = len(x)
    len_y = len(y)
    dis = []
    for l in range(m):
        len_x = len(x[l])
        x_row = x[l]
        if window is None:
            window = [(i, j) for i in range(len_x) for j in range(len_y)]
        window = ((i + 1, j + 1) for i, j in window)
        # 初始化矩阵中的其他元素为 inf 和 D[0, 0]=0；D使用元组记录矩阵的值
        D = defaultdict(lambda: (float('inf'),))
        D[0, 0] = (0, 0, 0)
        # 按照公式进行规划计算
        for i, j in window:

            if i == 1:
                k1 = derivative_distance(x_row[0], x_row[1], x_row[2])
            elif i == len_x:
                k1 = derivative_distance(x_row[len_x - 3], x_row[len_x - 2], x_row[len_x - 1])
            else:
                k1 = derivative_distance(x_row[i - 2], x_row[i - 1], x_row[i])
            if j == 1:
                k2 = derivative_distance(y[0], y[1], x_row[2])
            elif j == len_y:
                k2 = derivative_distance(y[len_y - 3], y[len_y - 2], x_row[len_y - 1])
            else:
                k2 = derivative_distance(y[j - 2], y[j - 1], x_row[j])

            dt = dist(k1, k2)
            D[i, j] = min((D[i - 1, j][0] + dt, i - 1, j), (D[i, j - 1][0] + dt, i, j - 1),
                          (D[i - 1, j - 1][0] + dt, i - 1, j - 1), key=lambda a: a[0])
        dis.append(D[len_x, len_y][0])
    sort_dis = sorted(dis)
    top_K = []
    for i in range(k):
        top_K.append(x[dis.index(sort_dis[i])])
    return top_K, sort_dis[0:k]


# 近似一阶导数
def derivative_distance(x, y, z):
    return ((y -x) + ((z - x) / 2)) / 2


# Weighted Dynamic Time Warping
def Wdtw(x, y, k, window=None):
    """
        @param x 序列1，可以是数据或是矩阵
        @param y 序列2，待匹配的目标序列
        @param window 序列设置要走的范围，默认为None会将矩阵遍历一遍
        @param dist 自定义距离计算方法，可以是欧氏距离，汉明距离等等
        @param k 返回与目标序列相似度最高的 K 条序列
    """
    m = len(x)
    len_y = len(y)
    dis = []
    for l in range(m):
        len_x = len(x[l])
        x_row = x[l]
        if window is None:
            window = [(i, j) for i in range(len_x) for j in range(len_y)]
        window = ((i + 1, j + 1) for i, j in window)
        # 初始化矩阵中的其他元素为 inf 和 D[0, 0]=0；D使用元组记录矩阵的值
        D = defaultdict(lambda: (float('inf'),))
        D[0, 0] = (0, 0, 0)
        # 按照公式进行规划计算
        for i, j in window:
            dt = weight_distance(i - 1, x_row[i - 1], j - 1, y[j - 1])
            D[i, j] = min((D[i - 1, j][0] + dt, i - 1, j), (D[i, j - 1][0] + dt, i, j - 1),
                          (D[i - 1, j - 1][0] + dt, i - 1, j - 1), key=lambda a: a[0])
        dis.append(D[len_x, len_y][0])
    sort_dis = sorted(dis)
    top_K = []
    for i in range(k):
        top_K.append(x[dis.index(sort_dis[i])])
    return top_K, sort_dis[0:k]


# 加权欧氏距离
def weight_distance(x1, y1, x2, y2):
    # 可能出现 x1 == x2 的情况，所以统一给权重加1
    weigt = abs(x2 - x1) + 1
    return weigt * abs(y2 - y1)


# 差值绝对值
def Euclidean_distance_abs(x, y):
    return abs(x-y)


# 差值平方
def Euclidean_distance_square(x, y):
    return (y-x) * (y-x)


if __name__ == '__main__':
    x = [[1, 2, 3, 4, 5]]
    y = [2, 3, 4]
    # x, dis = ED(x, y, Euclidean_distance_abs, 1)
    # x, dis = dtw_origin(x, y, Euclidean_distance_abs, 1, None)
    # x, dis = Ddtw(x, y, Euclidean_distance_square, 1, None)
    # x, dis = Wdtw(x, y, 1, None)
    x, dis = dtw_fast(x, y, Euclidean_distance_abs, 1, 1, None)

    print(x)
    print(dis)
