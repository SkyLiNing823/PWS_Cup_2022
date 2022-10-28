import random
import os
from rr_v1 import *
from dp_v2_001 import *

import multiprocessing as mp


def top_f(df, cols=[0], thetas=[80]):
    for i in range(len(cols)):
        df[df[cols[i]] > thetas[i]] = thetas[i]
    return df


def bottom_f(df, cols=[4], thetas=[1]):
    for i in range(len(cols)):
        df[df[cols[i]] < thetas[i]] = thetas[i]
    return df


def rr_f(df, q=0.2, target=[1, 2], randomseed=31):
    random.seed(randomseed)
    df2 = rrdf(df, q, target)
    return df2


def dp_f(df, cols=[0], epss=[0.1], randomseed=31):
    for i in range(len(cols)):
        df.iloc[:, cols[i]] = lap(df.iloc[:, cols[i]], epss[i], randomseed)
    return df


def listGen(timesBot, timesTop, colBot, colTop):
    L = []
    for i in range(random.randint(timesBot, timesTop)):
        i = random.randint(colBot, colTop)
        while (i in L):
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
        Q = (random.randint(1, 9)) / 10
        Target = listGen(1, 13, 0, 12)
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
        log += f'rr.py {Q} {list2log(Target)} {RandSeed}\n'
    elif number == 1:
        Cols = listGen(1, 13, 0, 12)
        Epss = []
        for i in range(len(Cols)):
            Epss.append((random.randint(1, 10))/10)
        df = dp_f(df, cols=Cols, epss=Epss, randomseed=RandSeed)
        log += f'dp2.py {list2log(Cols)} {list2log(Epss)} {RandSeed}\n'
    elif number == 2:
        Cols = [0]
        Thetas = [random.randint(80, 80), random.randint(80, 80)]
        df = top_f(df, cols=Cols, thetas=Thetas)
        log += f'top2.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 3:
        Cols = [0]
        Thetas = [random.randint(20, 30)]
        df = bottom_f(df, cols=Cols, thetas=Thetas)
        log += f'bottom2.py {list2log(Cols)} {list2log(Thetas)}\n'
    return df, log


def start(i, N, InputFilename, RandSeed):
    orderList = [_ for _ in range(2)]

    random.shuffle(orderList)
    df = pd.read_csv(InputFilename, header=None)
    log = ''
    for element in orderList:
        df, log = execute(df, log, element, RandSeed)
    path = f'generated/{InputFilename[:-4]}/{i+1}'
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
    InputFilename = f'ref_data{sys.argv[2]}.csv'
    RandSeed = 31
    if not os.path.exists('generated'):
        os.makedirs(f'generated')
    if not os.path.exists(f'generated/{InputFilename[:-4]}'):
        os.makedirs(f'generated/{InputFilename[:-4]}')
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores)
    for i in range(0, N, num_cores):
        Input = []
        for j in range(num_cores):
            Input.append((i+j, N, InputFilename, RandSeed))
        pool.starmap(start, Input)
    print('done')
