"""This module contains functions for extracting air quality data and loading it into Elasticsearch."""

from elasticsearch import Elasticsearch
from flask import jsonify, current_app
import requests


def normalize_coordinates(coords):
    """
        Normalize coordinates to be within the geographical bounds (-90, 90).

        Args:
            coords (list): List of coordinate values.

        Returns:
            list: Normalized list of coordinates.
    """
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

    response = requests.get(url, headers=headers, params=params)

    current_app.logger.info(f'Status ES request: {response.status_code}')

    total_records = None
    if response.status_code == 200:
        json_response = response.json()

        total_records = json_response['records']
        current_app.logger.info(f'Total Records: {total_records}')

    else:
        print("Response Body:", response.content)
        current_app.logger.error(f'Error fetching data. Status code: {response.status_code}')
        return jsonify({'error': 'Failed to fetch data'}), 500

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
                current_app.logger.info(f'inserting records: {record}')
                result = client.index(index=index_name, document=record)
                current_app.logger.info(f'Data indexed with ID: {result["_id"]}')
    except Exception as e:
        current_app.logger.error(f'Failed to index data: {str(e)}')

    return jsonify({'load success': 'Success to fetch data and load to ES'}), 200
