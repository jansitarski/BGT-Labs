import ray
import time
from faker import Faker
from google.cloud import datastore

def delete_all_test_data():
    """Function for Deleting all the Test data"""
    kind = 'BGTLab9'
    datastore_client = datastore.Client(project="bgt-labs-20701")
    fetch_limit = 100
    print('-- Deleting all entities --')
    entities = True
    while entities:
        query = datastore_client.query(kind=kind)
        entities = list(query.fetch(limit=fetch_limit))
        for entity in entities:
            #print('Deleting: {}'.format(entity))
            datastore_client.delete(entity.key)
    print('done')

delete_all_test_data()