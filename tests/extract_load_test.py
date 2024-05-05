import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from requests import HTTPError, Timeout

from fission_functions.air_quality_extract_load.airextract import main, normalize_coordinates

app = Flask(__name__)


class TestAirQualityFunctions(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app context
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Tear down the Flask app context
        self.app_context.pop()

    def test_normalize_coordinates(self):
        test_cases = [
            ([120, -130, 50], [60, -50, 50]),
            ([90, -90, 0], [90, -90, 0]),
            ([45, -45, 10], [45, -45, 10])
        ]
        for coords, expected in test_cases:
            with self.subTest(coords=coords):
                result = normalize_coordinates(coords)
                self.assertEqual(result, expected)

    @patch('fission_functions.air_quality_extract_load.airextract.requests.get')
    @patch('fission_functions.air_quality_extract_load.airextract.Elasticsearch')
    def test_main_success(self, mock_elasticsearch, mock_get):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            'records': [{'geometry': {'coordinates': [100, -100]}, 'siteName': 'Test Site'}]
        }
        mock_get.return_value = mock_response

        mock_es_instance = mock_elasticsearch.return_value
        mock_es_instance.index.return_value = {"_id": "1"}

        response, status_code = main()
        self.assertEqual(status_code, 200)
        self.assertIn('Successfully fetched data and loaded to Elasticsearch',
                      response.json['load success'])
        mock_elasticsearch.assert_called_once()
        mock_es_instance.index.assert_called()

    @patch('fission_functions.air_quality_extract_load.airextract.requests.get')
    def test_main_http_error(self, mock_get):
        mock_get.side_effect = MagicMock(side_effect=HTTPError("HTTP error occurred"))

        response, status_code = main()
        self.assertEqual(status_code, 500)
        self.assertIn('HTTP error occurred', response.json['error'])

    @patch('fission_functions.air_quality_extract_load.airextract.requests.get')
    def test_main_timeout(self, mock_get):
        mock_get.side_effect = Timeout()

        response, status_code = main()
        self.assertEqual(status_code, 408)
        self.assertIn('The request timed out', response.json['error'])


if __name__ == '__main__':
    unittest.main()
