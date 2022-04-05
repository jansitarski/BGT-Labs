#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python pip git
pip install dask[complete]
pip install pyarrow
export PATH="/home/s20701/.local/bin:$PATH"
git clone https://github.com/jansitarski/BGT-Labs
cd BGT-Labs/Lab04/


