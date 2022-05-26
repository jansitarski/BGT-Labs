import time

from google.cloud import datastore

datastore_client = datastore.Client(project="bgt-labs-20701")
datastore_kind = 'BGTNonSequential'
datastore_kind_sequential = 'BGTSequential'

def sum(kind):
    amount_sum = 0
    query = datastore_client.query(kind=kind)
    query.projection = ["Amount"]  # Projection Query
    query_iter = query.fetch()
    for entity in query_iter:
        amount_sum += entity["Amount"]
    print("Sum: ", amount_sum)


def median(kind):
    query = datastore_client.query(kind=kind)
    query.order = ["Amount"]
    query.keys_only()
    query_iter = query.fetch()
    count = 0
    # Count how many entries in kind
    for _ in query_iter:
        count += 1
    middle_index_set = {int(count/2-0.5)+1, int(count/2+0.4)+1}   # Get 1 or 2 middle indexes
    # Get median of two entries
    count = 0
    median = 0
    query2 = datastore_client.query(kind=kind)
    query.projection = ["Amount"]
    query2.order = ["Amount"]
    query_iter = query.fetch()
    for i in query_iter:  # Get
        count += 1
        for saved_index in middle_index_set:
            if saved_index == count:
                median += i["Amount"]
    result = median/len(middle_index_set)
    print("Median: ", result)
    return result


def big_earners(kind, name):
    query = datastore_client.query(kind=kind)
    query.add_filter('LastName', "=", name)
    query.add_filter('Amount', ">", median(kind)) # Could add projection amount
    query_iter = query.fetch()
    for entity in query_iter:
        print(entity)


def biggest_post_code(kind):
    query = datastore_client.query(kind=kind)
    query.projection = ["PostCode"]  # Projection Query
    query_iter = query.fetch()
    post_map = dict()
    for entity in query_iter:
        #print(entity["PostCode"])
        if entity["PostCode"] not in post_map:
            post_map[entity["PostCode"]] = 1
        else:
            post_map[entity["PostCode"]] += 1
    biggest_code = max(post_map,key=post_map.get)
    print(biggest_code,":", post_map[biggest_code])
    return biggest_code


def post_code_addresses(kind):
    query = datastore_client.query(kind=kind)
    query.add_filter('PostCode', "=", biggest_post_code(kind))
    #query.projection = ["PostCode","DeliveryAddress"]  # Projection Query
    query_iter = query.fetch()
    for entity in query_iter:
        print(entity["PostCode"],": ",entity["DeliveryAddress"]) # Cannot use projection on a property with an equality filter

start_time = time.time()
sum(datastore_kind)
print(time.time()-start_time)
print()
start_time = time.time()
median(datastore_kind)
print(time.time()-start_time)
print()
start_time = time.time()
big_earners(datastore_kind,"Blevins")
print(time.time()-start_time)
print()
start_time = time.time()
post_code_addresses(datastore_kind)
print(time.time()-start_time)
print()


start_time = time.time()
sum(datastore_kind_sequential)
print(time.time()-start_time)
print()
start_time = time.time()
median(datastore_kind_sequential)
print(time.time()-start_time)
print()
start_time = time.time()
big_earners(datastore_kind_sequential,"Blevins")
print(time.time()-start_time)
print()
start_time = time.time()
post_code_addresses(datastore_kind_sequential)
print(time.time()-start_time)
print()
