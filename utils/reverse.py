import numpy as np
df1 = np.loadtxt('JD-0.85.csv', dtype=np.int32)
count = 0
LEN = np.size(df1, 0)
for i in range(LEN):
    if df1[i] == 1:
        df1[i] = 0
    else:
        df1[i] = 1
np.savetxt('JD-0.852.csv', df1, fmt='%d')
