import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask import jsonify, current_app, Flask


def get_station_data(state):
    """ Fetches station data for a given state from BOM website. """
    url = f'https://reg.bom.gov.au/{state}/observations/{state}all.shtml'
    response = requests.get(url)
    if response.status_code != 200:
        current_app.logger.error(f"Failed to retrieve data for URL: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    all_data = soup.find_all('tr', class_="rowleftcolumn")
    stations = []

    for row in all_data:
        try:
            suffix = row.find('th', class_="rowleftcolumn").find('a')['href'].split('/')[3]
            station_idv, station_id = suffix.split('.')[0:2]
            station_name = row.find('th', class_="rowleftcolumn").find('a').text

            stations.append({
                'station_id': station_id,
                'station_name': station_name,
                'state': state,
                'url': f"http://www.bom.gov.au/fwo/{station_idv}/{station_idv}.{station_id}.json"
            })
        except Exception as e:
            current_app.logger.error(f"Error processing row: {e}")
            continue

    print (stations)
    return stations


def index_stations(stations):
    """ Indexes station data into Elasticsearch. """
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    index_name = "bom_stations"

    # Delete the index if it exists
    try:
        if client.indices.exists(index=index_name):
            client.indices.delete(index=index_name)
            current_app.logger.info(f"Deleted index: {index_name}")
    except Exception as e:
        current_app.logger.error(f"Failed to delete index: {e}")
        return "Index deletion failed", 500

    try:
        client.indices.create(
            index=index_name,
            body={
                "settings": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "station_id": {"type": "keyword"},
                        "station_name": {"type": "text"},
                        "state": {"type": "keyword"},
                        "url": {"type": "keyword"}
                    }
                }
            }
        )
        current_app.logger.info(f"Created index: {index_name}")
    except Exception as e:
        current_app.logger.error(f"Failed to create index: {e}")
        return "Index creation failed", 500

    actions = [
        {
            "_index": index_name,
            "_source": station
        }
        for station in stations
    ]

    try:
        successes, _ = bulk(client, actions)
        current_app.logger.info(f'Successfully indexed {successes} stations')
        return jsonify({'load success': f'Successfully indexed {successes} stations'}), 200
    except Exception as e:
        current_app.logger.error(f"Failed to bulk index stations due to {str(e)}")
        return jsonify({'error': 'Bulk index failed', 'details': str(e)}), 500


def main():
    states = ['nsw', 'vic', 'qld', 'wa', 'sa', 'tas', 'nt']
    all_stations = []
    for state in states:
        stations = get_station_data(state)
        all_stations.extend(stations)

    index_stations(all_stations)
    return jsonify({'finish process': 'Running OK'}), 200
