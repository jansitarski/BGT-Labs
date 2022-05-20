from google.cloud import datastore

datastore_client = datastore.Client(project="bgt-labs-20701")
datastore_kind = 'BGTNonSequentialLab11'

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

def commie_kill_list(kind, name):
    query = datastore_client.query(kind=datastore_kind)
    query.add_filter("Amount", ">", median(kind))
    query.add_filter("LastName", "=", "Adams")
    #query.projection = ["Amount"]  # Projection Query
    query_iter = query.fetch()
    for entity in query_iter:
        print(entity)


sum(datastore_kind)
median(datastore_kind)