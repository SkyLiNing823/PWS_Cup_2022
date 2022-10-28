# 和所有orig_data.csv & 所有tool程式放在同一層

import random
import os
from rr_v1 import *
from dp_v2_001 import *

import multiprocessing as mp


def rr_f(df, q=0.2, target=[1, 2], randomseed=31):
    random.seed(randomseed)
    df2 = rrdf(df, q, target)
    return df2


def dp_f(df, cols=[0], epss=[0.1], randomseed=31):
    np.random.seed(randomseed)
    for i in range(len(cols)):
        df.iloc[:, cols[i]] = lap(df.iloc[:, cols[i]], epss[i], randomseed)
    return df


def top_f(df, cols=[0], thetas=[80]):
    for i in range(len(cols)):
        df[df[cols[i]] > thetas[i]] = thetas[i]
    return df


def bottom_f(df, cols=[4], thetas=[1]):
    for i in range(len(cols)):
        df[df[cols[i]] < thetas[i]] = thetas[i]
    return df


def listGen(timesBot, timesTop, colBot, colTop):
    L = []
    for i in range(random.randint(timesBot, timesTop)):
        i = random.randint(colBot, colTop)
        while i in L:
            i = random.randint(colBot, colTop)
        L.append(i)
    L.sort()
    return L


def list2log(List):
    s = ''
    for i in List:
        s += str(i)+'_'
    return s[:-1]


def execute(df, number, RandSeed):
    if number == 0:
        Q = (random.randint(1, 9)) / 10
        Target = listGen(1, 13, 0, 12)
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
    elif number == 1:
        Cols = listGen(1, 13, 0, 12)
        Epss = []
        for i in range(len(Cols)):
            Epss.append((random.randint(1, 10))/10)
        df = dp_f(df, cols=Cols, epss=Epss, randomseed=RandSeed)
    elif number == 2:
        Cols = [0]
        Thetas = [random.randint(80, 80), random.randint(80, 80)]
        df = top_f(df, cols=Cols, thetas=Thetas)
    elif number == 3:
        Cols = [0]
        Thetas = [random.randint(20, 30)]
        df = bottom_f(df, cols=Cols, thetas=Thetas)
    return df


def start(i, N, dataSelect, RandSeed):
    s = 0
    while s == 0:
        orderList = [_ for _ in range(4)]
        random.shuffle(orderList)
        df = pd.read_csv(f'orig/orig_data{dataSelect}.csv', header=None)
        for element in orderList:
            df = execute(df, element, RandSeed)
        if df.shape[0] > 25:
            s = 1
        path = f'generated/orig_data{dataSelect}/{i+1}'
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_csv(
            f'{path}.csv', header=False, index=False)
    print(f'orig_data{dataSelect} : {i+1} / {N} is completed.\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], ' N')
        exit(-1)
    RandSeed = 31
    N = int(sys.argv[1])
    dataList = [1, 4, 9, 12, 21, 23, 25, 28,
                31, 37, 51, 64, 65, 69, 75, 79, 80, 120]
    for dataSelect in dataList:
        if not os.path.exists('generated'):
            os.makedirs(f'generated')
        if not os.path.exists(f'generated/orig_data{dataSelect}'):
            os.makedirs(f'generated/orig_data{dataSelect}')
        num_cores = int(mp.cpu_count())
        pool = mp.Pool(num_cores)
        for i in range(0, N, num_cores):
            Input = []
            for j in range(num_cores):
                Input.append((i+j, N, dataSelect, RandSeed))
            pool.starmap(start, Input)
        print('done')

    # if len(sys.argv) != 3:
    #     print(sys.argv[0], ' N dataSelect')
    #     exit(-1)
    # N = int(sys.argv[1])
    # dataSelect = sys.argv[2]
    # RandSeed = 31
    # if not os.path.exists('generated'):
    #     os.makedirs(f'generated')
    # if not os.path.exists(f'generated/orig_data{dataSelect}'):
    #     os.makedirs(f'generated/orig_data{dataSelect}')
    # num_cores = int(mp.cpu_count())
    # pool = mp.Pool(num_cores)
    # for i in range(0, N, num_cores):
    #     Input = []
    #     for j in range(num_cores):
    #         Input.append((i+j, N, dataSelect, RandSeed))
    #     pool.starmap(start, Input)
    # print('done')
