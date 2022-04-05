#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 pip git
sudo pip install dask[complete]
sudo pip3 install pyarrow
export PATH="/home/s20701/.local/bin:$PATH"
git clone https://github.com/jansitarski/BGT-Labs
cd BGT-Labs/Lab04/

mkdir data
gsutil -m cp gs://pjwstk-bigdata/*.parquet ./data/.

