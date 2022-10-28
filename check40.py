import numpy as np
import pandas as pd

RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
            'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']

for i in range(len(RefDataList)):
    output = np.array([0 for _ in range(80)])
    for j in range(len(RefDataList)):
        if i != j:
            orig = f'NE/ref_data_main_{RefDataList[i]}.csv'
            InputFilename = f'NE/ref_data_main_{RefDataList[j]}.csv'
            df = pd.read_csv(orig, header=None)
            target = pd.read_csv(InputFilename, header=None)
            count = 0
            LEN = np.size(target, 0)
            for t in range(LEN):
                if target.iloc[t].values.tolist() in df.values.tolist():
                    count += 1
                    output[t] = 1
            # if count >= 0:
            #     print('----------------------------------------------')
            #     print(f'{RefDataList[i]} vs {RefDataList[j]}')
            #     print(f'{count} / {LEN}')
    ccount = 0
    L = []
    for k in range(80):
        if output[k] == 0:
            L.append(k+1)
            ccount += 1
    print('----------------------------------------------')
    print(f'{TeamList[i]} : {L}')
    print(f'{ccount} / {LEN}')
    np.savetxt(f'zero/{TeamList[i]}.csv', output, fmt='%d')
