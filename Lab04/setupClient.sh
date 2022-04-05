#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip git
sudo pip3 install dask distributed --upgrade
sudo pip3 install pyarrow
git clone https://github.com/jansitarski/BGT-Labs
cd BGT-Labs/Lab04/

mkdir data
gsutil -m cp gs://pjwstk-bigdata/*.parquet ./data/.

