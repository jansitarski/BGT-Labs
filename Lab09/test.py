#!/usr/bin/env python3
from google.cloud import datastore
import ray
import time
from faker import Faker

ids = []
ray.init(address='192.168.0.10:6379')

@ray.remote
def f():
    datastore_client = datastore.Client(project="bgt-labs-20701")
    kind = 'BGTLab9'
    task_key = datastore_client.key(kind)
    fake = Faker()
    for _ in range(100):
        entity = datastore.Entity(key=task_key)
        entity['Name'] = fake.first_name()
        entity['Last Name'] = fake.last_name()
        entity['Address'] = fake.last_name()
        entity['Post Code'] = fake.postcode()
        entity['Delivery Address'] = fake.street_address()
        entity['Amount'] = fake.pricetag()
        datastore_client.put(entity)

completions_per_timestamp = []

for _ in range(100):
    print('iteration:', _)
    ids.append(f.remote())

ready, not_ready = ray.wait(ids)
all_scheaduled = not_ready
while True:
    _, not_ready = ray.wait(ids)
    print('Not Ready length:', len(not_ready))
    print('Done:', len(all_scheaduled) - len(not_ready))
    print('Done in 10s:', len(ids) - len(not_ready))
    completions_per_timestamp.append(len(ids)-len(not_ready))
    print()
    time.sleep(10)
    ids = not_ready
    if len(not_ready) == 0:
        break

print(completions_per_timestamp)