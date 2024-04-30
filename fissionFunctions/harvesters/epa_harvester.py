import requests
from flask import jsonify, current_app


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
    if response.status_code == 200:
        json_response = response.json()

        total_records = json_response['records'][0]
        current_app.logger.info(f'Total Records: {total_records}')
        return jsonify({'totalRecords': total_records})
    else:
        current_app.logger.error(f'Error fetching data. Status code: {response.status_code}')
        return jsonify({'error': 'Failed to fetch data'}), 500


