from google.cloud import datastore

datastore_client = datastore.Client(project="bgt-labs-20701")
kind = 'BGTNonSequentialLab11'
filters = []
query = datastore_client.query(kind='BGTNonSequentialLab11')


def nonsequential_sum():
    query_iter = query.fetch()
    query.projection = ["Amount"]  # Projection Query
    amount_sum = 0
    for entity in query_iter:
        amount_sum += entity["Amount"]
    print(amount_sum)


def nonsequential_median():
    query_iter = query.fetch()
    query.order = ["Amount"]
    query.keys_only()
    count = 0
    for entity in query_iter:
        count += 1
    # Get middle
    #offset in non 10001 is int(5000.5)+1
    print(count)
    query_iter.offset(count/2)
