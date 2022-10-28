import numpy as np
import pandas as pd
import random
import os


def remainCol(df, n):
    L = []
    for i in range(13):
        if i not in n:
            L.append(i)
    return df.drop(df.columns[L], axis=1)


TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
            'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                 '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
team = 'TI'
dataSelect = RefDataList[TeamList.index(team)]
AnonySelect = AnonyFileList[TeamList.index(team)]

if not os.path.exists('random40'):
    os.makedirs('random40')
if not os.path.exists(f'random40/{team}'):
    os.makedirs(f'random40/{team}')

orig = f'ANONY/{AnonySelect}'
# orig = 'DG17.csv'
InputFilename = f'NE/ref_data_main_{dataSelect}.csv'
# np.loadtxt(orig, dtype=np.int32, delimiter=',')
df = pd.read_csv(orig, header=None)
target = pd.read_csv(InputFilename, header=None)
memoryCol = []
memoryAns = []
probCol = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for i in range(1000000):
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
    for j in range(LEN):
        if remainCol(target, remainList).iloc[j].values.tolist() in remainCol(df, remainList).values.tolist():
            count += 1
            output[j] = 1
    if count == 40:
        # # if count >= 0 and count <= 433:
        # if remainList not in memoryCol:
        #     if output in memoryAns:
        #         print(f'{count} / {LEN}')
        #         print(remainList)
        #         for j in range(len(memoryAns)):
        #             if output == memoryAns[j]:
        #                 print(f'{memoryCol[j]}')
        #     else:
        #         print(remainList)
        #     print('----------------------------------------------')
        #     memoryCol.append(remainList)
        #     memoryAns.append(output)
        # if count >= 0 and count <= 433:
        # for j in range(len(memoryAns)):
        #     same = 0
        #     for k in range(LEN):
        #         if output[k] == memoryAns[j][k]:
        #             same += 1
        #     print(f'{remainList} vs {memoryCol[j]} : {same} / {LEN}')
        # print('----------------------------------------------')
        # memoryCol.append(remainList)
        # memoryAns.append(output)
        print('----------------------------------------------')
        print(f'{remainList} : {count} / {LEN}')
        memoryCol.append(remainList)
        memoryAns.append(output)
        np.savetxt(
            f'random40/{team}/{count}-{remainList}.csv', output, fmt='%d')
