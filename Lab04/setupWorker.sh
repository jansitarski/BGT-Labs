#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip git
pip install dask[complete]
pip install pyarrow

git clone https://github.com/jansitarski/BGT-Labs
cd BGT-Labs/Lab04/

mkdir data
gsutil -m cp gs://pjwstk-bigdata/*.parquet ./data/.
sudo cp -r data data2
sudo cp -r data data3

dask-worker 10.128.0.2:8786
