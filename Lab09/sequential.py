#!/usr/bin/env python3
import socket
from collections import Counter

from google.cloud import datastore
import ray
import time
from faker import Faker

ray.init(address='192.168.0.10:6379')


@ray.remote
class GlobalVarActor:
    def __init__(self):
        self.global_v = 1
    def set_global_v(self, v):
        self.global_v = v
    def get_global_v(self):
        return self.global_v


@ray.remote
class Dist:
    def __init__(self, global_v_registry):
        self.global_v_registry = global_v_registry
    def f(self):
        time.sleep(0.1)
        fake = Faker()
        datastore_client = datastore.Client(project="bgt-labs-20701")
        kind = 'BGTLab9'
        for i in range(100):
            index = ray.get(self.global_v_registry.get_global_v.remote())
            task_key = datastore_client.key(kind, index)
            ray.get(global_v_registry.set_global_v.remote(index + 1))
            entity = datastore.Entity(key=task_key)
            entity['Name'] = fake.first_name()
            entity['Last Name'] = fake.last_name()
            entity['Address'] = fake.last_name()
            entity['Post Code'] = fake.postcode()
            entity['Delivery Address'] = fake.street_address()
            entity['Amount'] = fake.pricetag()
            datastore_client.put(entity)
        return socket.gethostbyname(socket.gethostname())


global_v_registry = GlobalVarActor.remote()
counters = [Dist.remote(global_v_registry) for _ in range(100)]
ids = [c.f.remote() for c in counters]

ready, not_ready = ray.wait(ids)
all_scheaduled = not_ready

starttime = time.time()
completions_per_timestamp = []

while True:
    time.sleep(0.01)
    ready, not_ready = ray.wait(ids)
    # print('Not Ready length:', len(not_ready))
    # print('Done:', len(all_scheaduled) - len(not_ready))
    if (int(time.time() - starttime) % 10) == 1:
        time.sleep(1)
        print('Done in 10s:', len(all_scheaduled) - len(not_ready))
        completions_per_timestamp.append(len(all_scheaduled) - len(not_ready))
    ids = not_ready
    if len(not_ready) == 0:
        break

print(completions_per_timestamp)
