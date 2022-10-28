import numpy as np
import multiprocessing as mp
import sys


def record(L, InputFilename):
    with open(f'{InputFilename[:-4]}-MonteCarlo2.txt', 'w') as text_file:
        for i in range(50):
            text_file.write(f'{L[i]}\n')


def txt2answer(InputFilename):
    df = np.loadtxt(f'{InputFilename[:-4]}-MonteCarlo2.txt', dtype=np.int32)
    orderlist = [1 for _ in range(50)]
    for i in range(50//2):
        idx = np.unravel_index(np.argmax(df, axis=None), df.shape)
        df[idx] = 1
        orderlist[idx[0]] = 0
    for i in range(len(orderlist)):
        if orderlist[i] == 1:
            df[i] = 0
    np.savetxt(f'{InputFilename[:-4]}-answer2.csv', df, fmt='%d')


def start(i, N, target, dataSelect, InputFilename):
    subCountList = [0 for _ in range(50)]
    try:
        path = f'generated/ref_data{dataSelect}/{i+1}/{i+1}.csv'
        df = np.loadtxt(path, dtype=np.int32, delimiter=',')
        count = 0
        # df = np.delete(df, 3, axis=1)
        # target = np.delete(target, 3, axis=1)
        for j in range(50):
            # if df[j].tolist()[1:] in target[:, 1:].tolist():
            if df[j].tolist() in target.tolist():
                count += 1
                subCountList[j] += 1
        if count >= 20:
            with open(f'{InputFilename[:-4]}-highProb2.txt', 'a') as text_file:
                text_file.write(f'{path} : match {count} rows\n')
            print(f'{i+1}.csv is highly probable\n')
        print(f'{i+1} / {N} is checked.\n')
    except:
        print(f'{i+1} / {N} is out of range.\n')
    return subCountList


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(sys.argv[0],
              ' N InputFilename dataSelect')
        exit(-1)
    N = int(sys.argv[1])
    InputFilename = sys.argv[2]
    dataSelect = sys.argv[3]
    target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
    countList = [0 for _ in range(50)]
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores)
    for i in range(0, N, num_cores):
        record(countList, InputFilename)
        Input = []
        for j in range(num_cores):
            Input.append((i+j, N, target, dataSelect, InputFilename))
        subCountListCollect = pool.starmap(start, Input)
        for subCountList in subCountListCollect:
            countList = np.sum([countList, subCountList], axis=0).tolist()
    record(countList, InputFilename)
    txt2answer(InputFilename)
    print('done')
