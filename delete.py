# nojima for PWSCUP2022
import pandas as pd

filename = 'orig_data9.csv'
percent = 0.1
rows = round(300 * (1-percent))
df = pd.read_csv(filename, header=None)
# exclude_rows = list([i for i in range(rows)])
# df = df.drop(index=df.index[exclude_rows])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv(f'exclude-{1-percent}%.csv', header=False, index=False)
