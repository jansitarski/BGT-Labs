import dask.dataframe as dd
from dask.distributed import Client
import time
from dask_cloudprovider.gcp import GCPCluster

# gcsfs
if __name__ == "__main__":
    ##cluster = GCPCluster(on_host_maintenance="STOP", projectid="bgt-labs", n_workers=3, machine_type="e2-small", source_image="https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/debian-11-bullseye-v20220406")
    with GCPCluster(on_host_maintenance="STOP", env_vars=dict(EXTRA_PIP_PACKAGES="pyarrow"), projectid="bgt-labs-s20701",
                    n_workers=3, machine_type="e2-small") as cluster:
        with Client(cluster) as client:
            df = dd.read_parquet(
                ["gs://bucket_20701_bgt/data/*", "gs://bucket_20701_bgt/data2/*", "gs://bucket_20701_bgt/data3/*",
                 "gs://bucket_20701_bgt/data4/*"], storage_options={'anon': True, 'use_ssl': False}, engine="pyarrow")
            start_time = time.time()

            df = df['repo_name'].explode()

            df = df.value_counts(ascending=True)
            print(df.compute())
            print(client)

            print(time.time() - start_time, "seconds")
