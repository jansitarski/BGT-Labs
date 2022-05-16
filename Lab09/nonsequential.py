#!/usr/bin/env python3
import socket
from collections import Counter

from google.cloud import datastore
import ray
import time
from faker import Faker

ray.init(address='192.168.0.10:6379')

@ray.remote
def f():
    time.sleep(0.1)
    datastore_client = datastore.Client(project="bgt-labs-20701")
    kind = 'BGTLab9'
    task_key = datastore_client.key(kind)
    fake = Faker()
    for i in range(100):
        entity = datastore.Entity(key=task_key)
        entity['Name'] = fake.first_name()
        entity['Last Name'] = fake.last_name()
        entity['Address'] = fake.last_name()
        entity['Post Code'] = fake.postcode()
        entity['Delivery Address'] = fake.street_address()
        entity['Amount'] = fake.pricetag()
        datastore_client.put(entity)
    return socket.gethostbyname(socket.gethostname())


ids = [f.remote() for _ in range(100)]
ip_addresses = ray.get(ids)

print('Tasks assigned')
for ip_address, num_tasks in Counter(ip_addresses).items():
    print('    {} tasks on {}'.format(num_tasks, ip_address))

ready, not_ready = ray.wait(ids)
all_scheaduled = not_ready

starttime = time.time()
completions_per_timestamp = []

while True:
    time.sleep(0.01)
    ready, not_ready = ray.wait(ids)
    #print('Not Ready length:', len(not_ready))
    #print('Done:', len(all_scheaduled) - len(not_ready))
    if (int(time.time() - starttime)%10) == 1:
        time.sleep(1)
        print('Done in 10s:', len(all_scheaduled) - len(not_ready))
        completions_per_timestamp.append(len(all_scheaduled) - len(not_ready))
    ids = not_ready
    if len(not_ready) == 0:
        break

print(completions_per_timestamp)
