import json
import os
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch()

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, '../data/preprocessed_member_details.json')

with open(filepath, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")
    resp = helpers.bulk(
        client,
        data,
        index="parliament",
        doc_type="_doc"
    )
    print ("helpers.bulk() RESPONSE:", resp)

except Exception as err:
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()

query_all = {
    'size': 10000,
    'query': {
        'match_all': {}
    }
}

resp = client.search(
    index="parliament",
    body=query_all
)

# print ("search() response:", json.dumps(resp, indent=4, ensure_ascii=False))

print ("Length of docs returned by search():", len(resp['hits']['hits']))
