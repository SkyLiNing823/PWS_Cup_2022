# nojima for PWSCUP2022

import pandas as pd
import sys

if len(sys.argv) != 4:
    print("Usage : python [{}] 入力ファイル.csv 出力ファイル.csv  target_rows".format(sys.argv[0]))
    print("Example : python {} aaa.csv bbb.csv 0_1_2_3_4_5_6_7_8".format(sys.argv[0]))
    exit(-1)

    # exclude -  target_rows で与えられた行を削除する
    
df = pd.read_csv(sys.argv[1], header=None)
exclude_rows = list([int(i) for i in sys.argv[3].split("_")])
df = df.drop(index=df.index[exclude_rows])
df.to_csv(sys.argv[2], header=False, index=False)
