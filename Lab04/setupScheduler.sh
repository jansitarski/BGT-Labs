#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
sudo python3 -m pip install dask distributed --upgrade
echo hi > /test.txt
dask-scheduler --port 8000

