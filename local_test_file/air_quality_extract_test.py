from flask import Flask, jsonify, current_app
import requests

app = Flask(__name__)


@app.route('/fetch-data')
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

        total_records = json_response
        current_app.logger.info(f'Total Records: {total_records}')

    else:
        print("Response Body:", response.content)
        current_app.logger.error(f'Error fetching data. Status code: {response.status_code}')
        return jsonify({'error': 'Failed to fetch data'}), 500

    return total_records


if __name__ == '__main__':
    app.run(debug=True)
