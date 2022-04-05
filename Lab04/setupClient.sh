#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
sudo python3 -m pip install dask distributed --upgrade
pip3 install pyarrow

mkdir data
gsutil -m cp gs://pjwstk-bigdata/*.parquet ./data/.

