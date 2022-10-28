import random
import copy
import os
from kanony_v1 import *
from rr_v1 import *
from lap_v2 import *
from top_v1 import *
from bottom_v1 import *
import category_encoders as ce
import warnings
import shutil

import multiprocessing as mp


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


class Anony:
    def __init__(self, df, log, process, score):
        self.df = df
        self.log = log
        self.process = copy.deepcopy(process)
        self.score = score


def get_cor(mat, names):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        with np.errstate(invalid='ignore'):
            cor = np.corrcoef(mat.T)
            cor = cor * (np.ones(cor.shape) - np.diag(np.ones(cor.shape[0])))
        return pd.DataFrame(cor, columns=names, index=names).fillna(0)


def OneHot(df):
    categories = df.dtypes[df.dtypes == 'object'].index
    enc = ce.OneHotEncoder(
        cols=categories, drop_invariant=False, use_cat_names=True)
    enc.fit(df, ignore_index=True)
    df_value = enc.transform(df).astype("float64").values
    names = enc.get_feature_names()
    return df_value, names


def corBias(df, df2):
    df_value, names = OneHot(df)
    df_value2, names2 = OneHot(df2)
    cor = get_cor(df_value, names)
    cor2 = get_cor(df_value2, names2)
    return abs(cor.subtract(cor2).values.sum())


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
        filter = (orig[col] < low*10) | (orig[col] > high*10)
        filter2 = (df[col] < low*10) | (df[col] > high*10)
    else:
        filter = (orig[col] < low) | (orig[col] > high)
        filter2 = (df[col] < low) | (df[col] > high)
    count += abs(len(orig[filter])-len(df[filter2]))
    return count


def score(orig, anony):
    Score = 1
    count = 0
    for i in range(len(orig)):
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
    Score -= 0.001 * (300-len(anony))
    Score -= 0.1 * corBias(orig, anony)
    return Score


def list2log(List):
    s = ''
    for i in List:
        s += str(i)+'_'
    return s[:-1]


def getParameters(number):
    pList = []
    pList.append(number)
    if number == 0:  # kannoy
        pList.append(random.randint(2, 4))
        times = random.randint(1, 5)
        L = []
        for i in range(times):
            i = random.randint(0, 6)
            while i in L:
                i = random.randint(0, 6)
            L.append(i)
        L.sort()
        pList.append(L)
    elif number == 1:  # rr
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
    elif number == 2:  # lap
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
    elif number == 3:  # top2
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
    elif number == 4:  # bottom2
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
    elif number == 5:  # shuffle
        pList.append(random.randint(0, 100000))
    elif number == 6:  # top2_round
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
    elif number == 7:  # bottom2_round
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
    elif number == 8:  # average
        times = random.randint(2, 10)
        L = []
        for i in range(times):
            i = random.randint(0, 299)
            while i in L:
                i = random.randint(0, 299)
            L.append(i)
        L.sort()
        pList.append(L)
    elif number == 10:  # nn
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
        K = action[1]
        Qi = action[2]
        df = kanony_f(df, k=K, qi=Qi)
        log += f'kanony2.py {K} {list2log(Qi)}\n'
    elif number == 1:
        Q = action[1]
        Target = action[2]
        RandSeed = action[3]
        df = rr_f(df, q=Q, target=Target, randomseed=RandSeed)
        log += f'rr.py {Q} {list2log(Target)} {RandSeed}\n'
    elif number == 2:
        Cols = action[1]
        Epss = action[2]
        RandSeed = action[3]
        df = lap_f(df, cols=Cols, epss=Epss, randomseed=RandSeed)
        log += f'lap.py {list2log(Cols)} {list2log(Epss)} {RandSeed}\n'
    elif number == 3:
        Cols = action[1]
        Thetas = action[2]
        df = top_f(df, cols=Cols, thetas=Thetas)
        log += f'top2.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 4:
        Cols = action[1]
        Thetas = action[2]
        df = bottom_f(df, cols=Cols, thetas=Thetas)
        log += f'bottom2.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 5:
        RandSeed = action[1]
        df = shuffle_f(df, RandSeed)
        log += f'shuffle.py {RandSeed}\n'
    elif number == 6:
        Cols = action[1]
        Thetas = action[2]
        df = top2round_f(df, cols=Cols, thetas=Thetas)
        log += f'top2_round.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 7:
        Cols = action[1]
        Thetas = action[2]
        df = bottom2round_f(df, cols=Cols, thetas=Thetas)
        log += f'bottom2_round.py {list2log(Cols)} {list2log(Thetas)}\n'
    elif number == 8:
        try:
            Rows = action[1]
            df = average_f(df, rows=Rows)
            log += f'average.py {list2log(Rows)}\n'
        except:
            pass
    elif number == 9:
        df = ageLayering_f(df)
        log += f'age_layer.py\n'
    elif number == 10:
        try:
            Rows = action[1]
            Cols = action[2]
            df = nn_f(df, rows=Rows, cols=Cols)
            log += f'nn.py {list2log(Rows)} {list2log(Cols)}\n'
        except:
            pass
    return df, log


def start(anonyList, highScore, dataSelect, process):
    path = f'orig_data{dataSelect}'
    orig = pd.read_csv(f'orig/orig_data_main_{dataSelect}.csv', header=None)
    df = orig.copy()
    log = ''
    for i in range(len(process)):
        df, log = execute(df, log, process[i])
    df.columns = [
        'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
    orig.columns = [
        'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
    Score = score(orig, df)
    if Score > highScore.value:
        shutil.rmtree(path, ignore_errors=False, onerror=None)
        os.makedirs(path)
        df.to_csv(f'{path}/{int(round(Score*10000))}.csv',
                  header=False, index=False)
        with open(f'{path}/log.txt', "w") as text_file:
            text_file.write(log)
            highScore.value = Score
        print(f'High Score update to {highScore.value}. CSV is generated.')
    anonyList.append(Anony(df, log, process, Score))


def showScore(x):
    return x.score


def genEnd(anonyList, limit, generation):
    anonyList.sort(key=showScore, reverse=True)
    # environmental limit
    average = 0
    if len(anonyList) > limit:
        del anonyList[limit:]
    for anony in anonyList:
        average += anony.score
    average /= len(anonyList)
    print(
        f'GEN {generation}: highest = {anonyList[0].score}, average = {average}')
    return anonyList


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], ' dataSelect')
        exit(-1)
    dataSelect = sys.argv[1]
    # dataSelect = 9
    orig = pd.read_csv(f'orig/orig_data_main_{dataSelect}.csv', header=None)
    if not os.path.exists(f'orig_data{dataSelect}'):
        os.makedirs(f'orig_data{dataSelect}')
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores)
    highScore = mp.Value("d", -100.0)
    # parameters
    individual_limit = 120
    environmental_limit = 20
    new_limit = 40
    mate_Limit = 5
    heritable_P = 85
    loss_P = 10
    shuffle_P = 15
    mutate_P = 10
    anonyList = mp.Manager().list()
    actionList = [_ for _ in range(11)]
    generation = 1
    # first generation
    for i in range(environmental_limit):
        process = []
        action = random.choice(actionList)
        process.append(getParameters(action))
        Process = copy.deepcopy(process)
        p = mp.Process(target=start, args=(
            anonyList, highScore, dataSelect, Process))
        p.start()
        p.join()
    genEnd(anonyList, environmental_limit, generation)
    # evolution
    while True:
        generation += 1
        # new gene
        for i in range(new_limit):
            process = []
            action = random.choice(actionList)
            process.append(getParameters(action))
            Process = copy.deepcopy(process)
            p2 = mp.Process(target=start, args=(
                anonyList, highScore, dataSelect, Process))
            p2.start()
            p2.join()
        for i in range(len(anonyList)):
            if len(anonyList) >= individual_limit:
                break
            for child in range(mate_Limit):
                if len(anonyList) >= individual_limit:
                    break
                j = random.randint(0, len(anonyList)-1)
                if random.randint(1, 100) <= heritable_P and i != j:
                    # heritable
                    process = copy.deepcopy(anonyList[i].process)
                    rint = random.randint(0, len(anonyList[j].process)-1)
                    if anonyList[j].process[rint] in process:
                        for num in range(len(anonyList[j].process)):
                            if anonyList[j].process[num] not in process:
                                process.append(anonyList[j].process[num])
                    else:
                        process.append(anonyList[j].process[rint])
                    # loss gene
                    if random.randint(1, 100) <= loss_P and len(process) > 1:
                        del process[random.randint(0, len(process)-1)]
                    # shuffle
                    if random.randint(1, 100) <= shuffle_P:
                        random.shuffle(process)
                    # mutate
                    if random.randint(1, 100) <= mutate_P:
                        rint = random.randint(0, len(process)-1)
                        action = process[rint][0]
                        process[rint] = getParameters(action)
                    Process = copy.deepcopy(process)
                    p1 = mp.Process(target=start, args=(
                        anonyList, highScore, dataSelect, Process))
                    p1.start()
                    p1.join()
        genEnd(anonyList, environmental_limit, generation)
