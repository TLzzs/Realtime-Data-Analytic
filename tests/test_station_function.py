import unittest
from unittest.mock import patch

from flask import Flask

from fission_functions.weather_station_extract_load.weatherstationextract import get_station_data, index_stations


class TestGetStationData(unittest.TestCase):

    def setUp(self):
        """Set up a Flask app for testing."""
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Pop the Flask app context after the test runs."""
        self.app_context.pop()

    @patch('fission_functions.weather_station_extract_load.weatherstationextract.requests.get')
    def test_get_station_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = ('<html><tr class="rowleftcolumn"><th class="rowleftcolumn"><a '
                                      'href="/products/IDV60801/IDV60801.94839.shtml">Charlton</a></th></tr></html>')

        result = get_station_data('vic')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['station_id'], '94839')
        self.assertEqual(result[0]['station_name'], 'Charlton')

    @patch('fission_functions.weather_station_extract_load.weatherstationextract.requests.get')
    def test_get_station_data_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        result = get_station_data('vic')

        self.assertEqual(len(result), 0)

    @patch('fission_functions.weather_station_extract_load.weatherstationextract.Elasticsearch')
    @patch('fission_functions.weather_station_extract_load.weatherstationextract.bulk')
    def test_index_stations(self, mock_bulk, mock_es):
        mock_bulk.return_value = (1, [])

        mock_es.return_value.indices.exists.return_value = False
        mock_es.return_value.indices.create.return_value = None
        mock_es.return_value.indices.delete.return_value = None

        stations = [{'station_id': '123', 'station_name': 'Station Name', 'state': 'vic', 'url': 'http://example.com'}]

        response, status_code = index_stations(stations)

        # Assert checks
        self.assertEqual(status_code, 200)
        self.assertIn('Successfully indexed 1 stations', response.get_json()['load success'])

    @patch('fission_functions.weather_station_extract_load.weatherstationextract.Elasticsearch')
    def test_index_stations_failure(self, mock_es):
        mock_client = mock_es.return_value
        mock_client.indices.exists.side_effect = Exception("Failed to connect")

        stations = [{'station_id': '123', 'station_name': 'Station Name', 'state': 'vic', 'url': 'http://example.com'}]

        # Call the function
        response, status_code = index_stations(stations)

        self.assertEqual(status_code, 500)
        self.assertIn('Index deletion failed', response)


if __name__ == '__main__':
    unittest.main()
