from collections import defaultdict
import dask.dataframe as dd
import time
import pandas as pd

start_time = time.time()

# ./data.01.parquet is broken i guess
files = ['./data.00.parquet.gzip', './data.02.parquet.gzip', './data.03.parquet.gzip',
         './data.04.parquet.gzip', './data.05.parquet.gzip', './data.06.parquet.gzip',
         './data.07.parquet.gzip', './data.08.parquet.gzip', './data.09.parquet.gzip', './data.10.parquet.gzip']

df = dd.read_parquet(files)


repos = df["repo_name"].compute()

d = defaultdict(int)
for set in repos:
    for repo in set:
        d[repo] += 1

d = dict(sorted(d.items(), key=lambda x: x[1]))

df2 = pd.DataFrame.from_dict(d, orient='index')
print(df2)
print(time.time() - start_time, "seconds")