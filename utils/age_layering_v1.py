# wrote by nojima, 2022

import pandas as pd
import numpy as np
import sys

if len(sys.argv) != 3:
    print(sys.argv[0], ' input.csv output.csv')
    
df = pd.read_csv(sys.argv[1], header=None)
out = sys.argv[2]     

df.iloc[:, 0] = df.iloc[:,0]//10 * 10
df.to_csv(out, index = None, header = None)
