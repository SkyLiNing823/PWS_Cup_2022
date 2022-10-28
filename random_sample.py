# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import numpy as np
import random

seed = 100


def pick(a, b):
    one = np.ones(25)
    zero = np.zeros(25)
    df3 = np.array([[i for i in range(13)]])
    rList = np.concatenate((one, zero))
    np.random.shuffle(rList)
    for i in range(50):
        if rList[i] == 1:
            df3 = np.append(df3, [a[np.random.randint(a.shape[0]), :]], axis=0)
        else:
            # df3 = np.concatenate((df3, b[np.random.randint(b.shape[0]), :]))
            df3 = np.append(df3, [b[np.random.randint(b.shape[0]), :]], axis=0)
    return df3, rList


if __name__ == "__main__":
    n = 54
    a = f'orig/orig_data_main_{n}'+'.csv'
    # a = 'data_NB'+'.csv'
    b = 'data_none'+'.csv'
    output = f'ref_data{n}.csv'
    answer = f'ea{n}.csv'
    df = np.loadtxt(a, dtype=np.int32, delimiter=',')
    ex = np.loadtxt(b, dtype=np.int32, delimiter=',')
    dfc, ea = pick(df, ex)

    np.savetxt(output, dfc[1:],
               fmt='%d', delimiter=',')
    np.savetxt(answer, ea, fmt='%d')
