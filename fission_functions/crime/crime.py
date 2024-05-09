from elasticsearch import Elasticsearch
from flask import jsonify, request

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


#get crime by suburb name
def get_crime_by_suburb():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    suburb = request.headers.get("X-Fission-Params-Suburb")
    query = {
        "query": {
            "match": {
                "suburb_name": suburb
            }
        }
    }
    result = client.search(index="crime_test", body=query)
    crime = result["hits"]["hits"][0]['_source']
    return jsonify(crime)