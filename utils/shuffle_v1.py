# nojima for PWSCUP2022
import pandas as pd
import sys

if len(sys.argv) != 4:
    print("Usage : python [{}] 入力ファイル.csv 出力ファイル.csv [random seed]".format(sys.argv[0]))
    print("Example : python {} aaa.csv bbb.csv  121312".format(sys.argv[0]))
    exit(-1)
    # 行でシャッフルする。シードは, random seed としてあたえる.
    
df = pd.read_csv(sys.argv[1], header=None)
df2 =  df.sample(frac=1, random_state=int(sys.argv[3]))
df2.to_csv(sys.argv[2], header=False, index=False)
