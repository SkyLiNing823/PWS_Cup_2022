import numpy as np
import pandas as pd
n = 30
# orig = 'Full.csv'
# InputFilename = f'NE/ref_data{ns}.csv'
TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
            'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                 '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
team = 'MK'
dataSelect = RefDataList[TeamList.index(team)]
AnonySelect = AnonyFileList[TeamList.index(team)]
ref = pd.read_csv(f'NE/ref_data_main_{dataSelect}.csv', header=None)


def dropCol(df, n):
    L = []
    for i in range(13):
        if i not in n:
            L.append(i)
    return df.drop(df.columns[L], axis=1)


orig = 'PS-0.575.csv'  # 23
InputFilename = 'PS-0.725.csv'  # 29
df = pd.read_csv(orig, header=None)
count = 0
target = pd.read_csv(InputFilename, header=None)
LEN = np.size(target, 0)
for j in range(LEN):
    if target.iloc[j].values.tolist() != df.iloc[j].values.tolist():
        count += 1
        print(
            f'{j+1} : {df.iloc[j].values.tolist()} {target.iloc[j].values.tolist()}  {ref.iloc[j].values.tolist()}')
print('----------------------------------------------')
print(f'{count} / {LEN}')
