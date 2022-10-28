import numpy as np
import pandas as pd
import random


def remainCol(df, n):
    L = []
    for i in range(13):
        if i not in n:
            L.append(i)
    return df.drop(df.columns[L], axis=1)


orig = 'ANONY/tmp.csv'
# orig = 'DG17.csv'
InputFilename = 'NE/ref_data_main_14.csv'
# np.loadtxt(orig, dtype=np.int32, delimiter=',')
df = pd.read_csv(orig, header=None)
target = pd.read_csv(InputFilename, header=None)
output = np.array([0 for _ in range(80)])
for i in range(10000):
    count = 0
    rint = random.randint(1, 5)
    remainList = []
    while len(remainList) < rint:
        col = random.randint(0, 12)
        if col not in remainList:
            remainList.append(col)
        remainList.sort()
    LEN = np.size(target, 0)
    for j in range(LEN):
        if remainCol(target, remainList).iloc[j].values.tolist() in remainCol(df, remainList).values.tolist():
            count += 1
            output[j] = 1
    if count == 40:
        print('----------------------------------------------')
        print(remainList)
        print(f'{count} / {LEN}')
# np.savetxt('DG.csv', output, fmt='%d')
