import numpy as np

df = np.loadtxt(f'MonteCarlo.txt', dtype=np.int32)
check = np.array([0 for _ in range(80)])
for i in range(len(df)//2):
    idx = np.unravel_index(np.argmax(df, axis=None), df.shape)
    if(df[idx] > 10):
        df[idx] = 1
        check[idx] = 1
for i in range(len(df)):
    if check[i] != 1:
        df[i] = 0
np.savetxt(f'MM-answer.csv', df, fmt='%d')
