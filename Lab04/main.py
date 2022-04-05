import dask.dataframe as dd
from dask.distributed import Client
import time

if __name__ == "__main__":

    start_time = time.time()
    client = Client("10.128.0.2")

    df = dd.read_parquet("./data/new_0.parquet", engine="pyarrow")

    df = df['repo_name'].explode()
    df = df.value_counts(ascending=True)
    print(df.compute())
    print(client)

    print(time.time() - start_time, "seconds")