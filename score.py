import numpy as np
import pandas as pd


def countBias(orig, df, col, low, high):
    count = 0
    for item in range(low, high+1):
        if col == 'AGE':
            filter = (orig[col] >= item*10) & (orig[col] <= item*10+9)
            filter2 = (df[col] >= item*10) & (df[col] <= item*10+9)
        else:
            filter = (orig[col] == item)
            filter2 = (df[col] == item)
        count += abs(len(orig[filter])-len(df[filter2]))
    if col == 'AGE':
        filter = (orig[col] == item)
        filter2 = (df[col] < low*10) & (df[col] > high*10)
    else:
        filter = (orig[col] == item)
        filter2 = (df[col] < low) & (df[col] > high)
    count += abs(len(orig[filter])-len(df[filter2]))
    return count


def score(orig, anony):
    Score = 1
    count = 0
    LEN = np.size(orig, 0)
    for i in range(LEN):
        if orig.iloc[i].tolist() in anony.values.tolist():
            count += 1
    Score -= 0.1 * count
    bias = 0
    bias += countBias(orig, anony, 'AGE', 2, 8)
    bias += countBias(orig, anony, 'GENDER', 1, 2)
    bias += countBias(orig, anony, 'RACE', 1, 7)
    bias += countBias(orig, anony, 'INCOME', 1, 15)
    bias += countBias(orig, anony, 'EDUCATION', 1, 5)
    bias += countBias(orig, anony, 'VETERAN', 0, 1)
    bias += countBias(orig, anony, 'NOH', 1, 7)
    bias += countBias(orig, anony, 'HTN', 0, 1)
    bias += countBias(orig, anony, 'DM', 0, 1)
    bias += countBias(orig, anony, 'IHD', 0, 1)
    bias += countBias(orig, anony, 'CKD', 0, 1)
    bias += countBias(orig, anony, 'COPD', 0, 1)
    bias += countBias(orig, anony, 'CA', 0, 1)
    Score -= 0.0005 * bias
    Score -= 0.0001 * (300-len(anony))
    return Score


dataSelect = 9
orig = pd.read_csv(f'orig_data{dataSelect}.csv', header=None)
df = pd.read_csv(f'anony.csv', header=None)
df.columns = [
    'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
orig.columns = [
    'AGE', 'GENDER', 'RACE', 'INCOME', 'EDUCATION', 'VETERAN', 'NOH', 'HTN', 'DM', 'IHD', 'CKD', 'COPD', 'CA']
print(score(orig, df))
