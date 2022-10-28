# 和所有orig_data.csv & 所有tool程式放在同一層

import random
import os
from kanony_v1 import *
from rr_v1 import *
from dp_v2_001 import *
from top_v1 import *
from bottom_v1 import *

import multiprocessing as mp


def kanony_f(df, k=2, qi=[1, 2]):
    anonymized_df = kanony(df, qi=qi, k=k)
    return anonymized_df


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
    ex = True
    for i in range(len(cols)):
        ex &= (df.loc[:, int(cols[i])] < int(thetas[i]))
    ex = df[ex]
    return ex


def bottom_f(df, cols=[4], thetas=[1]):
    ex = True
    for i in range(len(cols)):
        ex &= (df.loc[:, int(cols[i])] > int(thetas[i]))
    ex = df[ex]
    return ex


def shuffle_f(df, randomseed=31):
    df2 = df.sample(frac=1, random_state=int(randomseed))
    return df2


def exclude_f(df, exclude_rows=[4]):
    df = df.drop(index=df.index[exclude_rows])
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


def execute(df, log, number, RandSeed):
    if number == 0:
        K = random.randint(2, 4)  # 2 8
        Qi = listGen(1, 5, 0, 6)
        df = kanony_f(df, k=K, qi=Qi)
        log += f'kanony2.py {K} {list2log(Qi)}\n'
    elif number == 1:
        Q = (random.randint(1, 9)) / 10
        Target = listGen(1, 13, 0, 12)
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
        log += f'rr.py {Q} {list2log(Target)} {RandSeed}\n'
    elif number == 2:
        Cols = listGen(1, 13, 0, 12)
        Epss = []
        for i in range(len(Cols)):
            Epss.append((random.randint(1, 10))/10)
        df = dp_f(df, cols=Cols, epss=Epss, randomseed=RandSeed)
        log += f'dp2.py {list2log(Cols)} {list2log(Epss)} {RandSeed}\n'
    elif number == 3:
        Cols = [0]
        Thetas = [random.randint(70, 80)]
        df = top_f(df, cols=Cols, thetas=Thetas)
        log += f'top2.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 4:
        Cols = [0]
        Thetas = [random.randint(20, 30)]
        df = bottom_f(df, cols=Cols, thetas=Thetas)
        log += f'bottom2.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 5:
        df = shuffle_f(df, RandSeed)
        log += f'shuffle.py {RandSeed}\n'
    return df, log


def start(i, N, dataSelect, RandSeed):
    s = 0
    while s == 0:
        orderList = [_ for _ in range(6)]
        random.shuffle(orderList)
        df = pd.read_csv(f'orig_data{dataSelect}.csv', header=None)
        log = ''
        for element in orderList:
            df, log = execute(df, log, element, RandSeed)
        if df.shape[0] > 25:
            s = 1
        path = f'generated/orig_data{dataSelect}/{i+1}'
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_csv(
            f'{path}/{i+1}.csv', header=False, index=False)
        with open(f'{path}/log.txt', "w") as text_file:
            text_file.write(log)
    print(f'{i+1} / {N} is completed.\n')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(sys.argv[0], ' N dataSelect')
        exit(-1)
    N = int(sys.argv[1])
    dataSelect = sys.argv[2]
    RandSeed = 31
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
