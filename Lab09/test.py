#!/usr/bin/env python3
from google.cloud import datastore
#import ray

import time
# Create & store an entity

#@ray.remote
def f():
    datastore_client = datastore.Client(project="bgt-labs-20701")
    # The kind for the new entity
    kind = 'namespacetest2'
    # The name/ID for the new entity
    ID = '5644004762845194'
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, ID)
    # Prepares the new entity
    testEntity = datastore.Entity(key=task_key)
    testEntity['Name'] = 'Rick Sanchez'
    testEntity['phone'] = '123123123'
    # Saves the entity
    datastore_client.put(testEntity)

f()