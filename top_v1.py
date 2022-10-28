# wrote by Hiroaki Kikuchi, 2021
# modified by nojima, 2022

import pandas as pd
import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(sys.argv[0], ' 入力ファイル.csv 出力ファイル.csv col theta ')
        sys.exit(0)
        # top coding - 列col でしきい値 theta より小さい行を出力する．列は 1_5 の様にベクトルで与えても良い．
    df = pd.read_csv(sys.argv[1], header=None)
    cols = sys.argv[3].split('_')
    thetas = sys.argv[4].split('_')

    ex = True

    for i in range(len(cols)):
        ex &= (df.loc[:, int(cols[i])] < int(thetas[i]))

    ex = df[ex]
    ex.to_csv(sys.argv[2], index=None, header=None)
