from elasticsearch import Elasticsearch
from flask import jsonify, current_app
import requests
from requests.exceptions import HTTPError, Timeout, RequestException


def normalize_coordinates(coords):
    normalized_coords = []
    for coord in coords:
        if coord > 90:
            normalized_coords.append(90 - (coord - 90))
        elif coord < -90:
            normalized_coords.append(-90 - (coord + 90))
        else:
            normalized_coords.append(coord)
    return normalized_coords


def main():
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites"
    headers = {
        "Host": "gateway.api.epa.vic.gov.au",
        "User-Agent": "curl/8.1.1",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "X-API-Key": "6d540a883a4c4fd4b3593be30499a204"
    }

    params = {
        "environmentalSegment": "air"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        json_response = response.json()
        total_records = json_response['records']
        current_app.logger.info(f'Total Records: {total_records}')
    except HTTPError as http_err:
        current_app.logger.error(f'HTTP error occurred: {http_err}')
        return jsonify({'error': 'HTTP error occurred', 'details': str(http_err)}), 500
    except Timeout:
        current_app.logger.error('The request timed out')
        return jsonify({'error': 'The request timed out'}), 408
    except RequestException as req_err:
        current_app.logger.error(f'Request error occurred: {req_err}')
        return jsonify({'error': 'Network related error', 'details': str(req_err)}), 500
    except ValueError:
        current_app.logger.error('Invalid response from API')
        return jsonify({'error': 'Invalid JSON response'}), 500

    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # Index data into Elasticsearch
    index_name = "air_quality"
    try:
        if isinstance(total_records, list):
            for record in total_records:
                coordinates = record["geometry"]["coordinates"]
                record["geometry"]["coordinates"] = normalize_coordinates(coordinates)
                result = client.index(index=index_name, document=record)
                current_app.logger.info(f'Data indexed with ID: {result["_id"]}')
    except Exception as e:
        current_app.logger.error(f'Unexpected error occurred: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

    return jsonify({'load success': 'Successfully fetched data and loaded to Elasticsearch'}), 200
