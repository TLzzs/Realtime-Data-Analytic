from elasticsearch import Elasticsearch
from flask import jsonify

#return all crime
def get_all_crime():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    query = {
        "query": {
            "match_all": {}
        }
    }
    result = client.search(index="crime_test", body=query)
    hits = result["hits"]["hits"]
    crimes = list(map(lambda h: h['_source'], hits))
    return jsonify(crimes)