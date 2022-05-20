#!/usr/bin/env python3
from google.cloud import datastore
import ray
import time
from faker import Faker

ray.init(address='192.168.0.10:6379')

@ray.remote
def f():
    datastore_client = datastore.Client(project="bgt-labs-20701")
    kind = 'BGTNonSequential'
    task_key = datastore_client.key(kind)
    fake = Faker()
    for i in range(100):
        entity = datastore.Entity(key=task_key)
        entity['Name'] = fake.first_name()
        entity['LastName'] = fake.last_name()
        entity['PostCode'] = fake.postcode()
        entity['DeliveryAddress'] = fake.street_address()
        entity['Amount'] = fake.pyfloat(right_digits=2, positive=True, min_value=1.0, max_value=10000.0)
        datastore_client.put(entity)


ids = [f.remote() for _ in range(100)]

ready, not_ready = ray.wait(ids,timeout=0)
all_scheaduled = not_ready
done_in_time = all_scheaduled

lasttime = time.time()
completions_per_timestamp = []

while True:
    ready, not_ready = ray.wait(ids, timeout=0)
    if time.time() - lasttime >= 10:
        print('Not Ready length:', len(not_ready))
        print('Done:', len(all_scheaduled) - len(not_ready))
        print('Done in 10s:', len(done_in_time) - len(not_ready))
        print()
        completions_per_timestamp.append(len(done_in_time) - len(not_ready))
        done_in_time = not_ready
        lasttime = time.time()
    ids = not_ready
    if len(not_ready) == 0:
        break

print(completions_per_timestamp)
