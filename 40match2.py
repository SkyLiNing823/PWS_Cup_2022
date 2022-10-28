import numpy as np
import pandas as pd
import random
import os
import sys
import multiprocessing as mp
import threading


def remainCol(df, n):
    L = []
    for i in range(13):
        if i not in n:
            L.append(i)
    return df.drop(df.columns[L], axis=1)


def known(output):
    zero = [3, 4, 11, 13, 24, 26, 38, 41, 42, 54, 55, 62, 72, 73, 77]
    count = 0
    for i in zero:
        if output[i-1] != 0:
            output[i-1] = 0
            count = count+1
    return count


def start(team):
    TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
                'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
    RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
    AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                     '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
    dataSelect = RefDataList[TeamList.index(team)]
    AnonySelect = AnonyFileList[TeamList.index(team)]
    orig = f'ANONY/{AnonySelect}'
    InputFilename = f'NE/ref_data_main_{dataSelect}.csv'
    df = pd.read_csv(orig, header=None)
    target = pd.read_csv(InputFilename, header=None)

    # INPUT
    probCol = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #
    count = 0
    rint = random.randint(1, len(probCol))
    remainList = []
    output = [0 for _ in range(80)]
    while len(remainList) < rint:
        col = random.choice(probCol)
        if col not in remainList:
            remainList.append(col)
        remainList.sort()
    LEN = np.size(target, 0)
    if 0 not in remainList:
        for j in range(LEN):
            if remainCol(target, remainList).iloc[j].values.tolist() in remainCol(df, remainList).values.tolist():
                output[j] = 1
    else:
        remainList.remove(0)
        AnonyFile = AnonyFileList[TeamList.index(team)]
        RefData = RefDataList[TeamList.index(team)]
        anony = np.loadtxt(f'ANONY/{AnonyFile}', dtype=np.int32, delimiter=',')
        ref = np.loadtxt(
            f'NE/ref_data_main_{RefData}.csv', dtype=np.int32, delimiter=',')
        for i in range(80):
            age = int(ref[i][0]/10) * 10
            LEN = np.size(anony, 0)
            for j in range(LEN):
                colCount = 0
                for col in remainList:
                    if anony[j][col] == ref[i][col]:
                        colCount += 1
                if colCount == len(remainList) and anony[j][col] == age:
                    output[i] = 1
                    break
        remainList.append(0)
    # if count == 40:
    diff = known(output)
    for i in range(len(output)):
        if output[i] == 1:
            count += 1
    if (count >= 30 and count <= 50) and diff < 5:
        print('----------------------------------------------')
        print(count)
        print(f'{remainList} : {count} / {LEN}')

        # INPUT
        InputFilename = f'test/PS-0.575.csv'  # 23
        InputFilename2 = f'test/PS-0.725.csv'  # 29
        InputFilename3 = 'test/PS-0.7.csv'  # 28
        InputFilename4 = 'test/PS-0.85.csv'  # 34
        #

        target = pd.read_csv(InputFilename, header=None)
        target2 = pd.read_csv(InputFilename2, header=None)
        target3 = pd.read_csv(InputFilename3, header=None)
        target4 = pd.read_csv(InputFilename4, header=None)
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        LEN = np.size(target, 0)
        for j in range(LEN):
            if target.iloc[j].values.tolist() != [output[j]]:
                count1 += 1
        print(f'DIFF1 : {count1} / {LEN}')
        for j in range(LEN):
            if target2.iloc[j].values.tolist() != [output[j]]:
                count2 += 1
        print(f'DIFF2 : {count2} / {LEN}')
        for j in range(LEN):
            if target3.iloc[j].values.tolist() != [output[j]]:
                count3 += 1
        print(f'DIFF3 : {count3} / {LEN}')
        for j in range(LEN):
            if target4.iloc[j].values.tolist() != [output[j]]:
                count4 += 1
        print(f'DIFF4 : {count4} / {LEN}')
        print(known(output))
        if abs(count1-23) == abs(count-40) and abs(count2-29) == abs(count-40) and abs(count3-28) == abs(count-40) and abs(count4-34) == abs(count-40):
            np.savetxt(
                f'random40/{team}/[{count}]={count1}-{count2}-{count3}-{count4}-{remainList}.csv', output, fmt='%d')


def thread_start(team):
    t_list = []
    n = 10
    for _ in range(n):
        t = threading.Thread(target=start, args=(team,))
        t_list.append(t)
    # 開始工作
    for t in t_list:
        t.start()
    # 調整多程順序
    for t in t_list:
        t.join()


if __name__ == '__main__':
    # INPUT
    team = 'PS'
    #
    print(team)
    if not os.path.exists('random40'):
        os.makedirs('random40')
    if not os.path.exists(f'random40/{team}'):
        os.makedirs(f'random40/{team}')

    MP_limit = int(mp.cpu_count())*3
    while True:
        p_list = []
        for i in range(MP_limit):
            p = mp.Process(target=thread_start, args=(team,))
            p_list.append(p)
        for p in p_list:
            p.start()
        for p in p_list:
            p.join()
