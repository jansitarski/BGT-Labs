#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python3 python3-pip
sudo pip3 install dask distributed --upgrade
dask-scheduler --port 8000

