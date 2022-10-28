import os
import numpy as np

path = 'AC'
path2 = 'AC2'
path3 = 'AC3'
fileList = os.listdir(path)
fileList2 = os.listdir(path2)
fileList3 = os.listdir(path3)

# output = np.zeros(80)
# print(output)
# for file in fileList:
#     anony = np.loadtxt(f'{path}/{file}', dtype=np.int32, delimiter=',')
#     for i in range(len(anony)):
#         output[i] += anony[i]

# for file in fileList2:
#     anony = np.loadtxt(f'{path2}/{file}', dtype=np.int32, delimiter=',')
#     for i in range(len(anony)):
#         output[i] += anony[i]

# for file in fileList3:
#     anony = np.loadtxt(f'{path3}/{file}', dtype=np.int32, delimiter=',')
#     for i in range(len(anony)):
#         output[i] += anony[i]

# output = output / (len(fileList) + len(fileList2) + len(fileList3))

# check = np.array([0 for _ in range(80)])
# for i in range(len(output)//2):
#     idx = np.unravel_index(np.argmax(output, axis=None), output.shape)
#     output[idx] = 1
#     check[idx] = 1
# for i in range(len(output)):
#     if check[i] != 1:
#         output[i] = 0
output = np.loadtxt(f'prefinal.csv', dtype=np.float32, delimiter=',')
output[output > 0.6108] = 1
output[output != 1] = 0
print(len(output[output == 1]))
print(output)
np.savetxt('final.csv', output, fmt='%d')
