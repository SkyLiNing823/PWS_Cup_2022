# Copyright 2020 Hiroaki Kikuchi 
import pandas as pd
import sys
import random
import numpy as np


def rr(x, q):
#     uniq = np.unique(x.values)
    uniq = x.value_counts().index.values
    y = [i if random.random() < q else random.choice(uniq) for i in x]
    return(y)


def rrdf(df, q, target):
    df2 = df.copy()
    for i in target:
        df2.iloc[:, i] = rr(df.iloc[:, i], q)
    return df2


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage : python [{}] 入力ファイル.csv 出力ファイル.csv [prob]  [target_columns] [random seed]".format(
            sys.argv[0]))
        print("Example : python {} aaa.csv bbb.csv 0.9 0_1_2_3_4_5_6_7_8 121312".format(
            sys.argv[0]))
        exit(-1)
    # ある列について、値毎に、確率 1 - q  で異なる値に変更する
    # 列はベクトル形式で指定することが可能
        
    random.seed(int(sys.argv[5]))
    df = pd.read_csv(sys.argv[1], header=None)
    q = float(sys.argv[3])
    target = list(set([int(i) for i in sys.argv[4].split("_")]))
    df2 = rrdf(df, q, target)
    df2.to_csv(sys.argv[2], header=False, index=False)
