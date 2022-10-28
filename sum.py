import numpy as np
import pandas as pd
import os

n = 6
output = np.array([0 for _ in range(80)])
for i in range(n):
    target = pd.read_csv(f'MM/22-{i+1}.csv', header=None)
    LEN = np.size(target, 0)
    for j in range(LEN):
        output[j] += target.iloc[j].values
print(output)
output = output/n
output[output >= 0.5] = 1
output[output < 1] = 0
print(len(output[output == 1.0]))
np.savetxt(f'MM/expect.csv', output, fmt='%d')
