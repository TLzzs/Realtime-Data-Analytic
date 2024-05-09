import requests
from elasticsearch import Elasticsearch, helpers
from flask import current_app, jsonify


def create_es_client():
    """Create and return an Elasticsearch client."""
    return Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )


def get_latest_record_time(client, station_id):
    """Retrieve the latest record's time from the Elasticsearch index for a specific station."""
    query = {
        "size": 1,
        "query": {"term": {"station_id.keyword": station_id}},
        "sort": [{"local_date_time_full": {"order": "desc"}}],
        "_source": ["local_date_time_full"]
    }
    response = client.search(index="bom_weather_data", body=query)
    if response['hits']['hits']:
        return response['hits']['hits'][0]['_source']['local_date_time_full']
    return None


def fetch_station_data(url):
    """Fetch weather data from the station's API."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=100)
    response.raise_for_status()
    return response.json()['observations']['data']


def filter_new_records(records, latest_time):
    """Filter out records older than the latest time."""
    if latest_time is not None:
        return [record for record in records if record['local_date_time_full'] > latest_time]
    return records


def bulk_load_to_es(client, actions):
    """Load a list of actions to Elasticsearch using the bulk API."""
    if actions:
        helpers.bulk(client, actions)
        return True, len(actions)
    return False, 0


def pre_processing(new_records, station_name, state, station_id):
    """Prepare the record by adding station details and removing unnecessary keys."""
    for record in new_records:
        record['station_name'] = station_name
        record['state'] = state
        record['station_id'] = station_id
        record.pop('sort_order', None)
    return new_records


def main():
    client = create_es_client()
    stations = client.search(index='bom_stations', body={"query": {"match_all": {}}}, size=1000)

    actions = []
    for station in stations['hits']['hits']:
        station_detail = station['_source']
        station_name = station_detail.get('station_name')
        state = station_detail.get('state')
        station_id = station_detail.get('station_id')
        try:
            latest_time = get_latest_record_time(client, station_id)
            current_app.logger.info(f"station: {station_name} has latest time of {latest_time}")

            weather_data = fetch_station_data(station_detail['url'])
            new_records = filter_new_records(weather_data, latest_time)

            current_app.logger.info(f"new weather data from {station_detail.get('station_name')} "
                                    f"need to be loaded: {len(new_records)}")

            pre_processing(new_records, station_name, state, station_id)
            actions.extend({
                               "_index": "bom_weather_data",
                               "_source": record
                           } for record in new_records)
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Network error for {station['_source']['station_name']}: {e}")
            continue
        except KeyError as e:
            current_app.logger.error(f"Data format error for {station['_source']['station_name']}: {e}")
            continue
        except Exception as e:
            current_app.logger.error(f"Unexpected error for {station['_source']['station_name']}: {e}")
            continue

    success, count = bulk_load_to_es(client, actions)
    if success:
        return jsonify({"message": f"Successfully loaded {count} new weather data entries.", "count": count}), 200
    return jsonify({"message": "No new data to load or bulk operation failed.", "count": count}), 200
