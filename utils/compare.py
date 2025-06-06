import numpy as np
import pandas as pd
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
team = 'PS'
L1 = [3, 5, 6, 7, 8, 12]
L2 = [3, 5, 6, 7, 8]

if not os.path.exists('random40'):
    os.makedirs('random40')
if not os.path.exists(f'random40/{team}'):
    os.makedirs(f'random40/{team}')

dataSelect = RefDataList[TeamList.index(team)]
AnonySelect = AnonyFileList[TeamList.index(team)]
orig = f'ANONY/{AnonySelect}'
InputFilename = f'NE/ref_data_main_{dataSelect}.csv'
df = pd.read_csv(orig, header=None)
target = pd.read_csv(InputFilename, header=None)
output1 = np.array([0 for _ in range(80)])
output2 = np.array([0 for _ in range(80)])
same = 0
count1 = 0
count2 = 0
LEN = np.size(target, 0)
for i in range(LEN):
    if remainCol(target, L1).iloc[i].values.tolist() in remainCol(df, L1).values.tolist():
        count1 += 1
        print(f'{i+1} : {target.iloc[i].values.tolist()}')
        output1[i] = 1
print('----------------------------------------------')
for i in range(LEN):
    if remainCol(target, L2).iloc[i].values.tolist() in remainCol(df, L2).values.tolist():
        count2 += 1
        print(f'{i+1} : {target.iloc[i].values.tolist()}')
        output2[i] = 1
for i in range(LEN):
    if output1[i] == output2[i]:
        same += 1
print('----------------------------------------------')
print(f'L1 : {count1} / {LEN}')
print(f'L2 : {count2} / {LEN}')
print(f'ID : {same} / {LEN}')
np.savetxt(f'random40/{team}/{count1}-{L1}.csv', output1, fmt='%d')
np.savetxt(f'random40/{team}/{count2}-{L2}.csv', output2, fmt='%d')
