# originally wrote by Hiroaki Kikuchi, 2021
# modified by nojima, 2022

import pandas as pd
import numpy as np
import sys

if len(sys.argv) != 5:
    print(sys.argv[0], ' input.csv d.csv  cols  epsilons')


    
df = pd.read_csv(sys.argv[1], header=None)
out = sys.argv[2]     
cols = [int(c) for c in sys.argv[3].split('_')]
chop = [int(e) for e in sys.argv[4].split('_')]

for i in range(len(cols)):
    df.iloc[df.iloc[:,cols[i]] >= chop[i], cols[i]] = chop[i] 
df.to_csv(out, index = None, header = None)


