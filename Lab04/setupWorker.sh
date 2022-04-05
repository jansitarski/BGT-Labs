#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
sudo python3 -m pip install dask distributed --upgrade
dask-worker 10.128.0.2:8000

gsutil -m cp gs://pjwstk-bigdata/*.parquet ./data/.

