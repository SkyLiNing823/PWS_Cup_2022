import numpy as np
import random
fileName = 'orig_data9.csv'
data = np.loadtxt(fileName, dtype=np.int32, delimiter=',')
AGE = data[:, 0]
RACE = data[:, 1]
GENDER = data[:, 2]


NOH = data[:, 6]
HTN = data[:, 7]
DM = data[:, 8]
IHD = data[:, 9]
CKD = data[:, 10]
COPD = data[:, 11]
CA = data[:, 12]
data = np.delete(data, np.where(AGE > 65)[0], axis=0)
INCOME = data[:, 3]
data = np.delete(data, np.where(INCOME > 15)[0], axis=0)
EDUCATION = data[:, 4]
data = np.delete(data, np.where(EDUCATION > 5)[0], axis=0)
VETERAN = data[:, 5]
data = np.delete(data, np.where(VETERAN > 1)[0], axis=0)

# data = EDUCATION[EDUCATION <= 5]
# data = VETERAN[VETERAN <= 1]
# INCOME[INCOME > 15] = 15
# EDUCATION[EDUCATION > 5] = 5
# VETERAN[VETERAN > 1] = 1

np.savetxt('test.csv', data, fmt='%d', delimiter=',')

# print(f'AGE < 65 : {np.where(AGE < 65)[0].size}')
# print(f'INCOME > 15 : {np.where(INCOME > 15)[0]}')
# print(f'EDUCATION > 5 : {np.where(EDUCATION > 5)[0]}')
# python cor.py orig_data79.csv orig_data79-cor.csv
