import numpy as np
df1 = np.loadtxt('JD1.csv', dtype=np.int32)
df2 = np.loadtxt('JD2.csv', dtype=np.int32)
count = 0
LEN = np.size(df1, 0)
for i in range(LEN):
    if df1[i] != df2[i]:
        count += 1
print(1-count/LEN)
