import random
import copy
import os
from kanony_v1 import *
from rr_v1 import *
from lap_v2 import *
import json

import multiprocessing as mp
import threading


def kanony_f(df, k, qi):
    anonymized_df = kanony(df, qi=qi, k=k)
    return anonymized_df


def rr_f(df, q, target, randomseed=31):
    random.seed(randomseed)
    df2 = rrdf(df, q, target)
    return df2


def lap_f(df, cols, epss, randomseed=31):
    np.random.seed(randomseed)
    for i in range(len(cols)):
        df.iloc[:, cols[i]] = lap(df.iloc[:, cols[i]], epss[i], randomseed)
    return df


def top_f(df, cols, thetas):
    ex = True
    for i in range(len(cols)):
        ex &= (df.loc[:, int(cols[i])] < int(thetas[i]))
    ex = df[ex]
    return ex


def bottom_f(df, cols, thetas):
    ex = True
    for i in range(len(cols)):
        ex &= (df.loc[:, int(cols[i])] > int(thetas[i]))
    ex = df[ex]
    return ex


def shuffle_f(df, randomseed):
    df2 = df.sample(frac=1, random_state=int(randomseed))
    return df2


def top2round_f(df, cols, thetas):
    for i in range(len(cols)):
        df.iloc[df.iloc[:, cols[i]] >= thetas[i], cols[i]] = thetas[i]
    return df


def bottom2round_f(df, cols, thetas):
    for i in range(len(cols)):
        df.iloc[df.iloc[:, cols[i]] <= thetas[i], cols[i]] = thetas[i]
    return df


def average_f(df, rows):
    avg = df.iloc[rows, :].mean().astype(int)
    for i in range(len(rows)):
        df.iloc[rows[i]] = avg
    return df


def ageLayering_f(df):
    df.iloc[:, 0] = df.iloc[:, 0]//10 * 10
    return df


def nn_f(df, rows, cols):
    for i in range(len(cols)):
        df.iloc[rows[i], cols[i]] = 99
    return df


def dropCol(df, n):
    return df.drop(df.columns[n], axis=1)


def score(df, AnonySelect, countList):
    Score = 0
    match = [0 for _ in range(80)]
    anony = pd.read_csv(f'ANONY/{AnonySelect}', header=None)
    for i in range(len(df)):
        if df.iloc[i].values.tolist()[1:] in anony.values[:, 1:].tolist():
            idx = anony.values[:, 1:].tolist().index(
                df.iloc[i].values.tolist()[1:])
            if int(df.iloc[i].values.tolist()[0] / 10) == int(anony.iloc[idx].values.tolist()[0] / 10):
                Score += 1
                match[i] += 1
                countList[i] += 1
    return Score, match


def list2log(List):
    s = ''
    for i in List:
        s += str(i)+'_'
    return s[:-1]


def getParameters(number):
    pList = []
    pList.append(number)
    if number == 0:  # rr
        pList.append(random.randint(1, 9)/10)
        times = random.randint(1, 13)
        L = []
        for i in range(times):
            i = random.randint(0, 12)
            while i in L:
                i = random.randint(0, 12)
            L.append(i)
        L.sort()
        pList.append(L)
        pList.append(random.randint(0, 100000))
    elif number == 1:  # lap
        times = random.randint(1, 13)
        L = []
        for i in range(times):
            i = random.randint(0, 12)
            while i in L:
                i = random.randint(0, 12)
            L.append(i)
        L.sort()
        pList.append(L)
        L2 = []
        for i in range(len(L)):
            L2.append((random.randint(1, 10))/10)
        pList.append(L2)
        pList.append(random.randint(0, 100000))
    elif number == 2:  # top2_round
        rint = random.randint(0, 12)
        if rint == 0:
            pList.append([0])
            pList.append([80])
        if rint == 1:
            pList.append([1])
            pList.append([2])
        if rint == 2:
            pList.append([2])
            pList.append([7])
        if rint == 3:
            pList.append([3])
            pList.append([15])
        if rint == 4:
            pList.append([4])
            pList.append([5])
        if rint == 5:
            pList.append([5])
            pList.append([1])
        if rint == 6:
            pList.append([6])
            pList.append([7])
        if rint == 7:
            pList.append([7])
            pList.append([1])
        if rint == 8:
            pList.append([8])
            pList.append([1])
        if rint == 9:
            pList.append([9])
            pList.append([1])
        if rint == 10:
            pList.append([10])
            pList.append([1])
        if rint == 11:
            pList.append([11])
            pList.append([1])
        if rint == 12:
            pList.append([12])
            pList.append([1])
    elif number == 3:  # bottom2_round
        rint = random.randint(0, 12)
        if rint == 0:
            pList.append([0])
            pList.append([20])
        if rint == 1:
            pList.append([1])
            pList.append([1])
        if rint == 2:
            pList.append([2])
            pList.append([1])
        if rint == 3:
            pList.append([3])
            pList.append([1])
        if rint == 4:
            pList.append([4])
            pList.append([1])
        if rint == 5:
            pList.append([5])
            pList.append([0])
        if rint == 6:
            pList.append([6])
            pList.append([1])
        if rint == 7:
            pList.append([7])
            pList.append([0])
        if rint == 8:
            pList.append([8])
            pList.append([0])
        if rint == 9:
            pList.append([9])
            pList.append([0])
        if rint == 10:
            pList.append([10])
            pList.append([0])
        if rint == 11:
            pList.append([11])
            pList.append([0])
        if rint == 12:
            pList.append([12])
            pList.append([0])
    elif number == 4:  # average
        times = random.randint(2, 10)
        L = []
        for i in range(times):
            i = random.randint(0, 299)
            while i in L:
                i = random.randint(0, 299)
            L.append(i)
        L.sort()
        pList.append(L)
    elif number == 6:  # nn
        L = []
        L2 = []
        L.append(random.randint(0, 299))
        L2.append(random.randint(0, 12))
        pList.append(L)
        pList.append(L2)
    return pList


def execute(df, log, action):
    number = action[0]
    if number == 0:
        Q = action[1]
        Target = action[2]
        RandSeed = action[3]
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
        log += f'rr.py {Q} {list2log(Target)} {RandSeed}\n'
    elif number == 1:
        Cols = action[1]
        Epss = action[2]
        RandSeed = action[3]
        df = lap_f(df, cols=Cols, epss=Epss, randomseed=RandSeed)
        log += f'lap.py {list2log(Cols)} {list2log(Epss)} {RandSeed}\n'
    elif number == 2:
        Cols = action[1]
        Thetas = action[2]
        df = top2round_f(df, cols=Cols, thetas=Thetas)
        log += f'top2_round.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 3:
        Cols = action[1]
        Thetas = action[2]
        df = bottom2round_f(df, cols=Cols, thetas=Thetas)
        log += f'bottom2_round.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 4:
        try:
            Rows = action[1]
            df = average_f(df, rows=Rows)
            log += f'average.py {list2log(Rows)}\n'
        except:
            pass
    elif number == 5:
        df = ageLayering_f(df)
        log += f'age_layer.py\n'
    elif number == 6:
        try:
            Rows = action[1]
            Cols = action[2]
            df = nn_f(df, rows=Rows, cols=Cols)
            log += f'nn.py {list2log(Rows)} {list2log(Cols)}\n'
        except:
            pass
    return df, log


def start(countList, highScore, dataSelect, team):
    path = f'MC_{team}'
    df = pd.read_csv(
        f'NE/ref_data_main_{dataSelect}.csv', header=None)
    rint = random.randint(1, 10)
    process = []
    for i in range(rint):
        action = random.choice(actionList)
        process.append(getParameters(action))
    log = ''
    for i in range(len(process)):
        df, log = execute(df, log, process[i])
    # df.columns = [
    #     'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
    Score, match = score(df, AnonySelect, countList)
    countList = np.sum([countList, match], axis=0).tolist()
    if Score > highScore.value:
        with open(f'{path}/log.txt', "w") as text_file:
            text_file.write(log)
        with open(f'{path}/{int(round(Score))}-{sum(match)}.csv', "w") as text_file:
            for i in range(80):
                text_file.write(f'{match[i]}\n')
        df.to_csv(f'{path}/best-anony.csv', header=False, index=False)
        highScore.value = Score
        print(
            f'High Score update to {highScore.value} ( match = {sum(match)} ). CSV is generated.')


def thread_distribute(countList, highScore, dataSelect, team, count):
    t_list = []
    n = 10
    for _ in range(n):
        t = threading.Thread(target=start, args=(
            countList, highScore, dataSelect, team))
        t_list.append(t)
    # 開始工作
    for t in t_list:
        t.start()
    # 調整多程順序
    for t in t_list:
        t.join()
    count.value += n


def genEnd(count, countList, team):
    print(f'checked {count.value} files.')
    with open(f'MC_{team}/MonteCarlo.txt', 'w') as text_file:
        for i in range(80):
            text_file.write(f'{countList[i]}\n')
    with open(f'MC_{team}/MC_expect.txt', 'w') as text_file:
        for i in range(80):
            text_file.write(f'{round(countList[i]/int(count.value),4)}\n')
    df = np.array(countList)
    check = np.array([0 for _ in range(80)])
    for i in range(len(df)//2):
        idx = np.unravel_index(np.argmax(df, axis=None), df.shape)
        if(df[idx] > 10):
            df[idx] = 1
            check[idx] = 1
    for i in range(len(df)):
        if check[i] != 1:
            df[i] = 0
    np.savetxt(f'MC_{team}/{team}-answer.csv', df, fmt='%d')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(sys.argv[0], ' team (continue)')
        exit(-1)
    TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
                'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
    RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
    AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                     '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
    team = sys.argv[1]
    dataSelect = RefDataList[TeamList.index(team)]
    AnonySelect = AnonyFileList[TeamList.index(team)]
    print(f'Team Name : {team}')
    print(f'Anony File Name : {AnonySelect}')
    print(f'RefData Name : ref_data_main_{dataSelect}.csv')
    if not os.path.exists(f'MC_{team}'):
        os.makedirs(f'MC_{team}')
    ctn = (len(sys.argv) == 3)
    num_cores = int(mp.cpu_count())
    count = mp.Value("d", 0)
    highScore = mp.Value("d", 0)
    countList = mp.Manager().list([0 for _ in range(80)])
    actionList = [_ for _ in range(11)]
    MP_limit = num_cores*3
    while True:
        p_list = []
        for i in range(MP_limit):
            p = mp.Process(target=thread_distribute, args=(
                countList, highScore, dataSelect, team, count))
            p_list.append(p)
        for p in p_list:
            p.start()
        for p in p_list:
            p.join()
        genEnd(count, countList, team)
