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


def countBias(orig, df, col, low, high):
    count = 0
    for item in range(low, high+1):
        if col == 'AGE':
            filter = (orig[col] >= item*10) & (orig[col] <= item*10+9)
            filter2 = (df[col] >= item*10) & (df[col] <= item*10+9)
        else:
            filter = (orig[col] == item)
            filter2 = (df[col] == item)
        count += abs(len(orig[filter])-len(df[filter2]))
    if col == 'AGE':
        filter = (orig[col] == item)
        filter2 = (df[col] < low*10) & (df[col] > high*10)
    else:
        filter = (orig[col] == item)
        filter2 = (df[col] < low) & (df[col] > high)
    count += abs(len(orig[filter])-len(df[filter2]))
    return count


def score(orig, anony):
    Score = 1
    count = 0
    LEN = np.size(orig, 0)
    for i in range(LEN):
        if orig.iloc[i].tolist() in anony.values.tolist():
            count += 1
    Score -= 0.1 * count
    bias = 0
    bias += countBias(orig, anony, 'AGE', 2, 8)
    bias += countBias(orig, anony, 'GENDER', 1, 2)
    bias += countBias(orig, anony, 'RACE', 1, 7)
    bias += countBias(orig, anony, 'INCOME', 1, 15)
    bias += countBias(orig, anony, 'EDUCATION', 1, 5)
    bias += countBias(orig, anony, 'VETERAN', 0, 1)
    bias += countBias(orig, anony, 'NOH', 1, 7)
    bias += countBias(orig, anony, 'HTN', 0, 1)
    bias += countBias(orig, anony, 'DM', 0, 1)
    bias += countBias(orig, anony, 'IHD', 0, 1)
    bias += countBias(orig, anony, 'CKD', 0, 1)
    bias += countBias(orig, anony, 'COPD', 0, 1)
    bias += countBias(orig, anony, 'CA', 0, 1)
    Score -= 0.0005 * bias
    Score -= 0.0001 * (300-len(anony))
    return Score


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


def execute(df, log, number):
    if number == 0:
        K = random.randint(2, 4)  # 2 8
        Qi = listGen(1, 5, 0, 6)
        df = kanony_f(df, k=K, qi=Qi)
        log += f'kanony2.py {K} {list2log(Qi)}\n'
    elif number == 1:
        RandSeed = random.randint(0, 100000)
        Q = (random.randint(1, 9)) / 10
        Target = listGen(1, 13, 0, 12)
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
        log += f'rr.py {Q} {list2log(Target)} {RandSeed}\n'
    elif number == 2:
        RandSeed = random.randint(0, 100000)
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
        RandSeed = random.randint(0, 100000)
        df = shuffle_f(df, RandSeed)
        log += f'shuffle.py {RandSeed}\n'
    return df, log


def start(highScore, dataSelect):
    times = random.randint(0, 10)
    orderList = [_ for _ in range(6)]
    for time in range(times):
        num = random.choice([2])
        orderList.append(num)
    random.shuffle(orderList)
    path = f'orig_data{dataSelect}'
    orig = pd.read_csv(f'orig_data{dataSelect}.csv', header=None)
    df = orig.copy()
    # df = pd.read_csv(f'{path}/anony.csv', header=None)
    log = ''
    for element in orderList:
        df, log = execute(df, log, element)
    df.columns = [
        'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
    orig.columns = [
        'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
    Score = score(orig, df)
    # with highScore.get_lock():
    if Score > highScore.value:
        df.to_csv(
            f'{path}/anony.csv', header=False, index=False)
        with open(f'{path}/log.txt', "w") as text_file:
            text_file.write(log)
            highScore.value = Score
        print(f'High Score update to {highScore.value}. CSV is generated.')


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print(sys.argv[0], ' dataSelect')
    #     exit(-1)
    # dataSelect = sys.argv[2]
    dataSelect = 9
    if not os.path.exists(f'orig_data{dataSelect}'):
        os.makedirs(f'orig_data{dataSelect}')
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores)
    highScore = mp.Value("d", -100.0)
    # orig = pd.read_csv(f'orig_data{dataSelect}.csv', header=None)
    # orig.to_csv(
    #     f'orig_data{dataSelect}/anony.csv', header=False, index=False)
    while True:
        Input = []
        # for i in range(num_cores):
        #     RandSeed = random.randint(0, 100000)
        #     Input.append((highScore, dataSelect, RandSeed))
        # pool.starmap(start, Input)
        processes = [mp.Process(target=start, args=(
            highScore, dataSelect,)) for i in range(num_cores)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    print('done')
