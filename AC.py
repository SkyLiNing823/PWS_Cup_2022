from secrets import choice
import numpy as np
import pandas as pd
import os
import multiprocessing as mp
import threading
import random
import time

TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
            'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                 '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
team = 'PS'
dataSelect = RefDataList[TeamList.index(team)]
AnonySelect = AnonyFileList[TeamList.index(team)]


# def start(output, team):
#     count1 = 0
#     count2 = 0
#     count3 = 0
#     InputFilename = 'test/MM-0.8.csv'  # 32
#     InputFilename2 = 'test/MM-0.55.csv'  # 22
#     InputFilename3 = 'test/MM-0.5.csv'
#     target = pd.read_csv(InputFilename, header=None)
#     target2 = pd.read_csv(InputFilename2, header=None)
#     target3 = pd.read_csv(InputFilename3, header=None)
#     ref = pd.read_csv(f'NE/ref_data_main_{dataSelect}.csv', header=None)
#     # target2 = pd.read_csv(InputFilename2, header=None)
#     LEN = np.size(target, 0)
#     for j in range(LEN):
#         if target.iloc[j].values != output[j]:
#             count1 += 1
#     print(f'DIFF1 : {count1} / {LEN}')
#     for j in range(LEN):
#         if target2.iloc[j].values != output[j]:
#             count2 += 1
#     print(f'DIFF2 : {count2} / {LEN}')
#     for j in range(LEN):
#         if target3.iloc[j].values != output[j]:
#             count3 += 1
#     print(f'DIFF3 : {count3} / {LEN}')
#     print('----------------------------------------------')
#     if(count1 == 32 and count2 == 22 and count3 == 20):
#         np.savetxt(f'AC/{team}.csv', output, fmt='%d')

def start(team):
    while True:
        unknownL = [i for i in range(80)]
        output = np.array([0 for _ in range(80)])
        zeros = [3, 4, 11, 13, 24, 26, 38, 41, 42, 54, 55, 62, 72, 73, 77]
        for i in zeros:
            output[i-1] = 0
            unknownL.remove(i-1)
        one = []
        while len(one) != 40:
            row = random.choice(unknownL)
            if row not in one:
                one.append(row)
                unknownL.remove(row)
        for row in one:
            output[row] = 1
        for row in unknownL:
            output[row] = 0
        # c1 = 0
        # c2 = 0
        # for i in range(80):
        #     if output[i] == 1:
        #         c1 += 1
        #     else:
        #         c2 += 1
        # print(f'{c1}   {c2}')
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        InputFilename = f'test/PS-0.575.csv'  # 23
        InputFilename2 = f'test/PS-0.725.csv'  # 29
        InputFilename3 = 'test/PS-0.7.csv'  # 28
        InputFilename4 = 'test/PS-0.85.csv'  # 34
        # InputFilename5 = 'test/MM-0.75.csv'  # 30
        target = pd.read_csv(InputFilename, header=None)
        target2 = pd.read_csv(InputFilename2, header=None)
        target3 = pd.read_csv(InputFilename3, header=None)
        target4 = pd.read_csv(InputFilename4, header=None)
        # target5 = pd.read_csv(InputFilename5, header=None)
        ref = pd.read_csv(f'NE/ref_data_main_{dataSelect}.csv', header=None)
        # target2 = pd.read_csv(InputFilename2, header=None)
        LEN = np.size(target, 0)
        for j in range(LEN):
            if target.iloc[j].values != output[j]:
                count1 += 1
        for j in range(LEN):
            if target2.iloc[j].values != output[j]:
                count2 += 1
        for j in range(LEN):
            if target3.iloc[j].values != output[j]:
                count3 += 1
        for j in range(LEN):
            if target4.iloc[j].values != output[j]:
                count4 += 1
        # for j in range(LEN):
        #     if target5.iloc[j].values != output[j]:
        #         count5 += 1
        if abs(count1-23) == 0 and abs(count2-29) == 0 and abs(count3-28) == 0 and abs(count4-34) == 0:
            t = time.localtime()
            # 依指定格式輸出
            result = time.strftime("%H:%M:%S", t)
            print('find')
            np.savetxt(
                f'AC/{result}.csv', output, fmt='%d')


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
    if not os.path.exists('AC'):
        os.makedirs('AC')
    MP_limit = int(mp.cpu_count())*3
    ch = [1, 0]
    p_list = []
    for i in range(MP_limit):
        p = mp.Process(target=thread_start, args=(team,))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
