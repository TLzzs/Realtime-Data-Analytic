from elasticsearch import Elasticsearch, helpers
from flask import jsonify
import json


def create_es_client():
    """Create and return an Elasticsearch client."""
    return Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

def load_json_to_es(client, index_name,file_path):
    """Load a list of actions from a local JSON file to Elasticsearch using the bulk API."""
    # Load JSON data from a file
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    actions = [
        {
            "_index": index_name,
            "_source": record
        }
        for record in json_data
    ]

    if actions:
        helpers.bulk(client, actions)
        return True, len(actions)
    return False, 0


def main():
    client = create_es_client()

    index_name = 'crime_records'
    file_path = './data/2019_processed_output.json'

    success, count = load_json_to_es(client, index_name, file_path)
    if success:
        return jsonify({"message": f"Successfully loaded {count} new crime data entries.", "count": count}), 200
    return jsonify({"message": "No new data to load or bulk operation failed.", "count": count}), 200
