import numpy as np
import sys
import random
import os


def countRow(dataSelect, refSelect):
    if not os.path.exists(f'ref_data{refSelect}'):
        os.makedirs(f'ref_data{refSelect}')
    orig = f'orig/orig_data{dataSelect}.csv'
    InputFilename = f'NE/ref_data{refSelect}.csv'
    df = np.loadtxt(orig, dtype=np.int32, delimiter=',')
    output = np.array([0 for _ in range(50)])
    count = 0
    target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
    LEN = np.size(target, 0)
    for j in range(LEN):
        if target[j].tolist() in df.tolist():
            count += 1
            output[j] = 1
    print(f'{count} / {LEN}')
    np.savetxt(
        f'ref_data{refSelect}/{dataSelect}-answer.csv', output, fmt='%d')


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print(sys.argv[0],
    #           ' refSelect')
    #     exit(-1)
    # refSelect = sys.argv[1]
    refSelect = 5
    # orderList = [1, 4, 9, 12, 21, 23, 25, 28,
    #              31, 37, 51, 64, 65, 69, 75, 79, 80, 120]
    # for dataSelect in orderList:
    #     countRow(dataSelect, refSelect)
    count = 0
    s = 0
    while s == 0:
        count += 1
        df = np.array([0 for _ in range(50)])
        orderList = [1, 4, 9, 12, 21, 23, 25, 28,
                     31, 37, 51, 64, 65, 69, 75, 79, 80, 120]
        random.shuffle(orderList)
        for dataSelect in orderList:
            path = f'ref_data{refSelect}/{dataSelect}-answer.csv'
            df2 = np.loadtxt(path, dtype=np.int32, delimiter=',')
            for i in range(50):
                if df2[i] == 1:
                    df[i] = 1
            if np.sum(df == 1) >= 25:
                np.savetxt(
                    f'ref_data{refSelect}/{refSelect}-over25answer.csv', df, fmt='%d')
                break
            np.savetxt(
                f'ref_data{refSelect}/{refSelect}-not25answer.csv', df, fmt='%d')
        print(f'{count}')
        if np.sum(df == 1) == 25:
            np.savetxt(
                f'ref_data{refSelect}/{refSelect}-25answer.csv', df, fmt='%d')
            s = 1
            print('find the 25 answer.')
