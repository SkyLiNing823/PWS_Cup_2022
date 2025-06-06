# wrote by Hiroaki Kikuchi, 2021
# modified by nojima, 2022
# modified by Chida, 2022 8 29

import pandas as pd
import numpy as np
import sys

SEED = 0

#def lap(x, eps):
#    return (x + np.random.default_rng().laplace(0, 1/eps, x.shape[0])).astype(int) 
#    # intへのキャストは不要かも．sensitivity = 1とする．

#numpyのdefault_rngは明示的にseedを与える

def lap(x, eps, seed):
    return (x + np.random.default_rng(seed).laplace(0, 1/eps, x.shape[0])).astype(int) 


def lapdf(dfin, cols, epss):
    df = dfin.copy()
    for i in range(len(cols)):
        df.iloc[:,cols[i]] = lap(df.iloc[:,cols[i]], epss[i],seed)
    return df    

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(sys.argv[0], ' 入力ファイル.csv 出力ファイル.csv  cols  epsilons random_seed')
        exit(-1)

        # 差分プライバシーに基づいて列colsにepsilon のラプラスノイズを付加する．
        # 列及びepsilonについてはベクトル形式で指定することが可能
        # 乱数のseedは, random_seed で与える.
        
    SEED=int(sys.argv[5])
    np.random.seed(SEED)    
    df = pd.read_csv(sys.argv[1], header=None)
    cols = [int(c) for c in sys.argv[3].split('_')]
    epss = [float(e) for e in sys.argv[4].split('_')]
    out = sys.argv[2] if len(sys.argv) == 6 else sys.stdout
    for i in range(len(cols)):
        df.iloc[:,cols[i]] = lap(df.iloc[:,cols[i]], epss[i],SEED)
    df.to_csv(out, index = None, header = None)
