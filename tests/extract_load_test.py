import unittest
from flask import Flask, current_app
from unittest.mock import patch, MagicMock
from fission_functions.air_quality_extract_load.airextract import normalize_coordinates, main

app = Flask(__name__)


class TestAirQualityFunctions(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app context
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Tear down the Flask app context
        self.app_context.pop()

    # Test cases follow...

    @patch('requests.get')
    def test_main_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            'records': [{'geometry': {'coordinates': [100, -100]}, 'siteName': 'Test Site'}]
        }
        mock_get.return_value = mock_response

        # Test `main` function
        with patch('elasticsearch.Elasticsearch') as mock_es:
            mock_es().index.return_value = {"_id": "1"}
            response, status_code = main()
            self.assertEqual(status_code, 200)
            self.assertIn('Success to fetch data and load to ES', response.json['load success'])

    @patch('requests.get')
    def test_main_failure(self, mock_get):
        # Mock a failed API response
        mock_response = MagicMock(status_code=500, content=b"Internal Server Error")
        mock_get.return_value = mock_response

        # Test `main` function
        response, status_code = main()
        self.assertEqual(status_code, 500)
        self.assertIn('Failed to fetch data', response.json['error'])


if __name__ == '__main__':
    unittest.main()
