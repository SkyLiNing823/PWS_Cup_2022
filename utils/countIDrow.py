import numpy as np
import pandas as pd


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
team = 'TM'
dataSelect = RefDataList[TeamList.index(team)]
AnonySelect = AnonyFileList[TeamList.index(team)]
orig = f'ANONY/{AnonySelect}'
orig = f'MM/MM-1.csv'
# orig = 'DG17.csv'
InputFilename = f'NE/ref_data_main_{dataSelect}.csv'
# np.loadtxt(orig, dtype=np.int32, delimiter=',')
df = pd.read_csv(orig, header=None)
target = pd.read_csv(InputFilename, header=None)
output = np.array([0 for _ in range(80)])
count = 0
# np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
LEN = np.size(target, 0)
for j in range(LEN):
    # if target.iloc[j].values[:3].tolist() in df.values[:, :3].tolist():
    if remainCol(target, [0]).iloc[j].values.tolist() in remainCol(df, [0]).values.tolist():
        count += 1
        print(f'{j+1} : {target.iloc[j].values.tolist()}')
        output[j] = 1
print('----------------------------------------------')
print(f'{count} / {LEN}')
# np.savetxt('RH.csv', output, fmt='%d')
