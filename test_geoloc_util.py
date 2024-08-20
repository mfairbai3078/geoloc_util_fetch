import unittest
from unittest.mock import patch, MagicMock

__author__ = "Matthew Fairbairn"
__version__ = "1.0.0"
__maintainer__ = "Matthew Fairbairn"
__email__ = "fairbairn.matthew@gmail.com"
__status__ = "Demo"

class TestGeoLocationUtility(unittest.TestCase):

    @patch('requests.get')
    @patch('os.getenv', return_value='fake_api_key')
    def test_fetch_location_by_city_state(self, mock_getenv, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "Denver", "lat": 39.7392364, "lon": -104.984862,"place_name":"Denver"}
        ]
        mock_get.return_value = mock_response

        from geoloc_util import fetch_location_by_city_state
        result = fetch_location_by_city_state("Denver, CO", "fake_api_key")
        self.assertEqual(result['lat'], 39.7392364)
        self.assertEqual(result['lon'], -104.984862)
        self.assertEqual(result['place_name'],"Denver")

    @patch('requests.get')
    @patch('os.getenv', return_value='fake_api_key')
    def test_fetch_location_by_zip(self, mock_getenv, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"zip": "80129", "lat": 39.5397, "lon": -105.0109,"place_name":"Douglas County"}
        mock_get.return_value = mock_response

        from geoloc_util import fetch_location_by_zip
        result = fetch_location_by_zip("80129", "fake_api_key")
        self.assertEqual(result['lat'], 39.5397)
        self.assertEqual(result['lon'], -105.0109)
        self.assertEqual(result['place_name'],"Douglas County")


if __name__ == "__main__":
    unittest.main()
