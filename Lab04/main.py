import dask.dataframe as dd
from dask.distributed import Client, Scheduler
import time

if __name__ == "__main__":

    start_time = time.time()
    #cluster = LocalCluster()
    scheduler = Scheduler()
    client = Client(n_workers=1, threads_per_worker=2, memory_limit='4GB')

    df = dd.read_parquet("./data/new_0.parquet", engine="pyarrow")

    df = df['repo_name'].explode()
    df = df.value_counts(ascending=True)
    print(df.compute())
    print(client)

    print(time.time() - start_time, "seconds")