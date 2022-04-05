import dask.dataframe as dd
from dask.distributed import Client
import time

if __name__ == "__main__":
    start_time = time.time()
    client = Client()

    df = dd.read_parquet("./data/new_*.parquet", engine="pyarrow")
    df2 = dd.read_parquet("./data2/new_*.parquet", engine="pyarrow")
    df3 = dd.read_parquet("./data3/new_*.parquet", engine="pyarrow")

    df = df['repo_name'].explode()
    df2 = df2['repo_name'].explode()
    df3 = df3['repo_name'].explode()

    df = dd.concat([df, df2, df3], 0)
    df = df.value_counts(ascending=True)
    print(df.compute())
    print(client)

    print(time.time() - start_time, "seconds")
