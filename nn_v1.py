# wrote by nojima, 2022

import pandas as pd
import numpy as np
import sys


if len(sys.argv) != 5:
    print(sys.argv[0], ' input.csv anon.csv  rows  columns')
    sys.exit(0)
    
df = pd.read_csv(sys.argv[1], header=None)
rows = [int(c) for c in sys.argv[3].split('_')]
cols = [int(e) for e in sys.argv[4].split('_')]
out = sys.argv[2] 

for i in range(len(cols)):
    df.iloc[rows[i],cols[i]] = 99
df.to_csv(out, index = None, header = None)

