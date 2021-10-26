# import Python's JSON library for its loads() method
import json
import os

# use the Elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, '../data/preprocessed_member_details.json')

with open(filepath, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# attempt to index the dictionary entries using the helpers.bulk() method
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    resp = helpers.bulk(
        client,
        data,
        index="test",
        doc_type="_doc"
    )

    # print the response returned by Elasticsearch
    print ("helpers.bulk() RESPONSE:", resp)

except Exception as err:

    # print any errors returned w
    # Prerequisiteshile making the helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()

# get all of docs for the index
# Result window is too large, from + size must be less than or equal to: [10000]
query_all = {
    'size': 10_000,
    'query': {
        'match_all': {}
    }
}

# pass the query_all dict to search() method
resp = client.search(
    index="test",
    body=query_all
)

print ("search() response:", json.dumps(resp, indent=4))

# print the number of docs in index
print ("Length of docs returned by search():", len(resp['hits']['hits']))
