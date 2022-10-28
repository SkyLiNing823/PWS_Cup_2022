from secrets import choice
import numpy as np
import os
import multiprocessing as mp
import threading
import random


def start(team):
    TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
                'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
    RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
    AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                     '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
    dataSelect = RefDataList[TeamList.index(team)]
    AnonyFile = AnonyFileList[TeamList.index(team)]
    anony = np.loadtxt(f'ANONY/{AnonyFile}', dtype=np.int32, delimiter=',')
    ref = np.loadtxt(
        f'NE/ref_data_main_{dataSelect}.csv', dtype=np.int32, delimiter=',')

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    while(count1 != 26 or count2 != 20 or count3 != 22 or count4 != 20):
        if os.path.exists(f'AC/{team}.csv'):
            break
        t = 0
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        output = np.array([0 for _ in range(80)])
        one = []
        zero = [i for i in range(80)]
        for i in range(len(ref)):
            age = int(ref[i][0]/10) * 10
            f1 = ref[i][7]
            f2 = ref[i][8]
            f3 = ref[i][9]
            f4 = ref[i][10]
            f5 = ref[i][11]
            f6 = ref[i][12]
            LEN = np.size(anony, 0)
            for j in range(LEN):
                if anony[j][0] == age and anony[j][7] == f1 and anony[j][8] == f2 and anony[j][9] == f3 and anony[j][10] == f4 and anony[j][11] == f5 and anony[j][12] == f6:
                    t += 1
                    # print(f'{i+1} : {ref[i]}')
                    output[i] = 1
                    one.append(i)
                    zero.remove(i)
                    break
        one2zero = []
        zero2one = []
        output[1-1] = 0
        output[8-1] = 0
        output[42-1] = 0
        # output[46-1] = 0
        output[49-1] = 0
        output[50-1] = 0
        output[70-1] = 0
        # output[77-0] = 0
        one.remove(1-1)
        one.remove(8-1)
        one.remove(42-1)
        one.remove(46-1)
        one.remove(49-1)
        one.remove(50-1)
        one.remove(70-1)
        one.remove(77-1)
        while(len(one2zero) < 12):
            n = random.choice(one)
            if n not in one2zero:
                one2zero.append(n)
        while(len(zero2one) < 2):
            n = random.choice(zero)
            if n not in zero2one:
                zero2one.append(n)
        for index in one2zero:
            output[index] = 0
        for index in zero2one:
            output[index] = 1

        # print(f'{t} / 80')
        InputFilename = 'test/MK-0.65.csv'  # 26
        InputFilename2 = 'test/MK-0.5.csv'  # 20
        InputFilename3 = 'test/MK-0.55.csv'  # 22
        InputFilename4 = 'test/MK-0.52.csv'  # 20
        target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
        target2 = np.loadtxt(InputFilename2, dtype=np.int32, delimiter=',')
        target3 = np.loadtxt(InputFilename3, dtype=np.int32, delimiter=',')
        target4 = np.loadtxt(InputFilename4, dtype=np.int32, delimiter=',')
        LEN = np.size(target, 0)
        for j in range(LEN):
            if target[j] != output[j]:
                count1 += 1
        # print(f'DIFF1 : {count1} / {LEN}')
        for j in range(LEN):
            if target2[j] != output[j]:
                count2 += 1
        # print(f'DIFF2 : {count2} / {LEN}')
        for j in range(LEN):
            if target3[j] != output[j]:
                count3 += 1
        # print(f'DIFF3 : {count3} / {LEN}')
        for j in range(LEN):
            if target4[j] != output[j]:
                count4 += 1
        # print(f'DIFF4 : {count4} / {LEN}')
        # print('----------------------------------------------')
        s = 1
        for j in range(LEN):
            if output[j] == 1 and ref[j][0] <= 55:
                count1 += 100
    if(count1 == 26 and count2 == 20 and count3 == 22 and count4 == 20):
        print('find')
        np.savetxt(f'AC/{team}.csv', output, fmt='%d')

# def start(team):
#     while True:
#         output = np.array([0 for _ in range(80)])
#         output[3-1] = 0
#         output[6-1] = 1
#         output[9-1] = 1
#         output[12-1] = 0
#         output[14-1] = 1
#         output[15-1] = 0
#         output[16-1] = 0
#         output[17-1] = 1
#         output[19-1] = 0
#         output[20-1] = 1
#         output[21-1] = 0
#         output[22-1] = 0
#         output[23-1] = 0
#         output[26-1] = 0
#         output[28-1] = 0
#         output[29-1] = 1
#         output[31-1] = 0
#         output[33-1] = 0
#         output[35-1] = 0
#         output[39-1] = 0
#         output[40-1] = 0
#         output[43-1] = 0
#         output[45-1] = 0
#         output[48-1] = 0
#         output[50-1] = 0
#         output[51-1] = 0
#         output[52-1] = 0
#         output[56-1] = 1
#         output[58-1] = 0
#         output[59-1] = 0
#         output[60-1] = 0
#         output[61-1] = 0
#         output[63-1] = 0
#         output[65-1] = 1
#         output[66-1] = 0
#         output[72-1] = 0
#         output[73-1] = 0
#         output[76-1] = 0
#         output[77-1] = 0
#         output[78-1] = 0
#         unknownL = [1, 2, 4, 5, 7, 8, 10, 11, 13, 18, 24, 25, 27, 30, 32, 34, 36, 37, 38, 41, 42,
#                     44, 46, 47, 49, 53, 54, 55, 57, 62, 64, 67, 68, 69, 70, 71, 74, 75, 79, 80]
#         one = []
#         while len(one) != 32:
#             row = random.choice(unknownL)
#             if row not in one:
#                 one.append(row)
#         for row in one:
#             output[row-1] = 1
#         L = [0 for _ in range(40)] + [1 for _ in range(40)]
#         output = np.array(L)
#         np.random.shuffle(output)
#         count1 = 0
#         count2 = 0
#         count3 = 0
#         count4 = 0
#         count5 = 0
#         InputFilename = 'test/JD-0.85.csv'  # 34
#         InputFilename2 = 'test/JD-0.975.csv'  # 39
#         # InputFilename3 = 'test/JD-0.852.csv'  # 34
#         # InputFilename4 = 'test/MM-0.7.csv'  # 28
#         # InputFilename5 = 'test/MM-0.75.csv'  # 30
#         target = pd.read_csv(InputFilename, header=None)
#         target2 = pd.read_csv(InputFilename2, header=None)
#         # target3 = pd.read_csv(InputFilename3, header=None)
#         # target4 = pd.read_csv(InputFilename4, header=None)
#         # target5 = pd.read_csv(InputFilename5, header=None)
#         ref = pd.read_csv(f'NE/ref_data_main_{dataSelect}.csv', header=None)
#         # target2 = pd.read_csv(InputFilename2, header=None)
#         LEN = np.size(target, 0)
#         for j in range(LEN):
#             if target.iloc[j].values != output[j]:
#                 count1 += 1
#         for j in range(LEN):
#             if target2.iloc[j].values != output[j]:
#                 count2 += 1
#         # for j in range(LEN):
#         #     if target3.iloc[j].values != output[j]:
#         #         count3 += 1
#         # for j in range(LEN):
#         #     if target4.iloc[j].values != output[j]:
#         #         count4 += 1
#         # for j in range(LEN):
#         #     if target5.iloc[j].values != output[j]:
#         #         count5 += 1
#         if(count1 == 34 and count2 == 39):
#             # if(abs(count1-32) <= 4 and abs(count2-22) <= 4 and abs(count3-20) <= 4 and abs(count4-28) <= 4 and abs(count5-30) <= 4):
#             print('find')
#             np.savetxt(f'AC/{team}.csv', output, fmt='%d')
#         # np.savetxt(
#         #     f'AC/{abs(count1-32)}-{abs(count2-22)}-{abs(count3-20)}-{abs(count4-28)}-{abs(count5-30)}.csv', output, fmt='%d')
#         if os.path.exists(f'AC/{team}.csv'):
#             break


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
    team = 'MK'
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
