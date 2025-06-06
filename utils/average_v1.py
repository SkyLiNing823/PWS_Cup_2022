# modified by nojima, 2022

import pandas as pd
import numpy as np
import sys

if len(sys.argv) != 4:
    print(sys.argv[0], ' input.csv anon.csv rows')
    
df = pd.read_csv(sys.argv[1], header=None)
out = sys.argv[2]     
rows = [int(c) for c in sys.argv[3].split('_')]

avg = df.iloc[rows,:].mean().astype(int)

for i in range(len(rows)):
    df.iloc[rows[i]] = avg
df.to_csv(out, index = None, header = None)
