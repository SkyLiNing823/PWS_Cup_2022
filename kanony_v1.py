#nojima based on Hiroaki Kikuchi for PWSCUP2022

import pandas as pd
import sys

def kanony(df, qi=[1, 2], k=1):
    return df.groupby(qi).filter(lambda x: x[0].count() >= k)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(sys.argv[0], ' 入力ファイル.csv　出力.csv col k ')        
        sys.exit(0)
        # k 匿名化 - 列col を準識別子としてk匿名化する．列は 1_5 の様にベクトルで与えても良い．



    df = pd.read_csv(sys.argv[1], header=None)
    k = int(sys.argv[3])
    qi = list(set([int(i) for i in sys.argv[4].split("_")]))

    anonymized_df = kanony(df, qi=qi, k=k)
    anonymized_df.to_csv(sys.argv[2], header=False, index=False)

