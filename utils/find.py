import random
import numpy as np

TeamList = ['AY', 'DG', 'HK', 'JD', 'KM', 'MK',
            'MM', 'ND', 'PM', 'PS', 'RF', 'RH', 'TI', 'TM']
RefDataList = [61, 17, 63, 34, 65, 21, 7, 8, 70, 26, 27, 13, 14, 15]
AnonyFileList = ['output.csv', 'ano17.csv', 'orig_data63_output.csv', '0929_JD_ver6_orig_data34.csv', 'main_data65_Kogeki_Shinaide.csv', 'data_21_final.csv',
                 '7_2022-1002-112655.csv', '20221003220051_data_main_8.csv', 'anon_data_main_70.csv', 'out_2.csv', 'anon_data_main_27.csv', 'anon_data13.csv', 'tmp.csv', 'anony_data_main_15.csv']
team = 'RF'
AnonyFile = AnonyFileList[TeamList.index(team)]
RefData = RefDataList[TeamList.index(team)]

anony = np.loadtxt(f'ANONY/{AnonyFile}', dtype=np.int32, delimiter=',')

# age = 50
# f1 = 1
# f2 = 0
# f3 = 0
# f4 = 1
# f5 = 0
# f6 = 0

# LEN = np.size(ref, 0)
# for i in range(LEN):
#     if anony[i][0] == age and anony[i][7] == f1 and anony[i][8] == f2 and anony[i][9] == f3 and anony[i][10] == f4 and anony[i][11] == f5 and anony[i][12] == f6:
#         print(f'{i+1} {ref[i]}')

ref = np.loadtxt(
    f'NE/ref_data_main_{RefData}.csv', dtype=np.int32, delimiter=',')
count1 = 0
count2 = 0
count3 = 0
count4 = 0

t = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
output = np.array([0 for _ in range(80)])
one = []
zero = [i for i in range(80)]
for i in range(len(ref)):
    age = int(ref[i][0]/10) * 10
    L = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12]  # 0,1,6
    LEN = np.size(anony, 0)
    for j in range(LEN):
        colCount = 0
        for col in L:
            if anony[j][col] == ref[i][col]:
                colCount += 1
        if colCount == len(L):
            t += 1
            print(f'{i+1} : {ref[i]}')
            output[i] = 1
            break
print(f'{t} / 80')
np.savetxt('RF/RF.csv', output, fmt='%d')
# np.savetxt('ND/NDfinal.csv', output, fmt='%d')
