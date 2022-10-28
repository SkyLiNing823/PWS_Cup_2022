import numpy as np
import multiprocessing as mp
import sys
import os


def record(L, dataSelect, refSelect):
    with open(f'ref_data{refSelect}/{dataSelect}-MonteCarlo.txt', 'w') as text_file:
        for i in range(300):
            text_file.write(f'{L[i]}\n')


def countRow(dataSelect, refSelect):
    orig = f'orig/orig_data{dataSelect}.csv'
    InputFilename = f'NE/ref_data{refSelect}.csv'
    df = np.loadtxt(orig, dtype=np.int32, delimiter=',')
    output = np.array([0 for _ in range(50)])
    count = 0
    target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
    LEN = np.size(target, 0)
    MC = np.loadtxt(
        f'ref_data{refSelect}/{dataSelect}-MonteCarlo.txt', dtype=np.int32, delimiter=',')
    for i in range(300):
        for j in range(LEN):
            if target[j].tolist() == df[i].tolist():
                print(f'{j+1} : {target[j].tolist()}')
                if MC[i] >= 1:
                    count += 1
                    output[j] = 1
        print(f'{count} / {LEN}')
        np.savetxt(
            f'ref_data{refSelect}/{dataSelect}-answer.csv', output, fmt='%d')


def start(i, N, target, dataSelect):
    subCountList = [0 for _ in range(300)]
    try:
        path = f'generated/orig_data{dataSelect}/{i+1}.csv'
        df = np.loadtxt(path, dtype=np.int32, delimiter=',')
        count = 0
        for j in range(300):
            if df[j].tolist()[1:] in target[:, 1:].tolist():
                count += 1
                subCountList[j] += 1
        print(f'orig_data{dataSelect} : {i+1} / {N} is checked.\n')
    except:
        print(f'orig_data{dataSelect} : {i+1} / {N} is out of range.\n')
    return subCountList


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(sys.argv[0],
              ' N InputFilename refSelect')
        exit(-1)
    N = int(sys.argv[1])
    InputFilename = sys.argv[2]
    refSelect = sys.argv[3]
    if not os.path.exists(f'ref_data{refSelect}'):
        os.makedirs(f'ref_data{refSelect}')
    target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
    num_cores = int(mp.cpu_count())
    pool = mp.Pool(num_cores)
    dataList = [1, 4, 9, 12, 21, 23, 25, 28,
                31, 37, 51, 64, 65, 69, 75, 79, 80, 120]
    for dataSelect in dataList:
        countList = [0 for _ in range(300)]
        for i in range(0, N, num_cores):
            record(countList, dataSelect, refSelect)
            Input = []
            for j in range(num_cores):
                Input.append((i+j, N, target, dataSelect))
            subCountListCollect = pool.starmap(start, Input)
            for subCountList in subCountListCollect:
                countList = np.sum([countList, subCountList], axis=0).tolist()
        record(countList, dataSelect, refSelect)
        countRow(dataSelect, refSelect)
    print('done')

# if __name__ == '__main__':
#     if len(sys.argv) != 5:
#         print(sys.argv[0],
#               ' N InputFilename dataSelect refSelect')
#         exit(-1)
#     N = int(sys.argv[1])
#     InputFilename = sys.argv[2]
#     dataSelect = sys.argv[3]
#     refSelect = sys.argv[4]
#     target = np.loadtxt(InputFilename, dtype=np.int32, delimiter=',')
#     countList = [0 for _ in range(300)]
#     num_cores = int(mp.cpu_count())
#     pool = mp.Pool(num_cores)
#     for i in range(0, N, num_cores):
#         record(countList, InputFilename, dataSelect)
#         Input = []
#         for j in range(num_cores):
#             Input.append((i+j, N, target, dataSelect))
#         subCountListCollect = pool.starmap(start, Input)
#         for subCountList in subCountListCollect:
#             countList = np.sum([countList, subCountList], axis=0).tolist()
#     record(countList, InputFilename, dataSelect)
#     countRow(dataSelect, refSelect)
#     print('done')
