__author__ = "Matthew Fairbairn"
__version__ = "1.0.0"
__maintainer__ = "Matthew Fairbairn"
__email__ = "fairbairn.matthew@gmail.com"
__status__ = "Demo"
import pytest
import os
from unittest.mock import patch, MagicMock
from geoloc_util import get_api_key, fetch_location_by_city_state, fetch_location_by_zip, get_location_data

# Mock responses
mock_city_state_response = [
    {
        "name": "Denver",
        "lat": 43.0731,
        "lon": -89.4012,
    }
]

mock_zip_response = {
    "lat": 40.7128,
    "lon": -74.0060,
    "zip": "12345"
}


@pytest.fixture
def valid_api_key():
    return "valid_api_key"


@pytest.fixture
def invalid_api_key():
    return None


@pytest.fixture
def mock_args():
    return MagicMock(api_key=None, locations=["Madison, WI", "12345"])


# Test get_api_key function
def test_get_api_key_with_env_variable(valid_api_key):
    with patch.dict(os.environ, {"API_KEY": valid_api_key}):
        assert get_api_key(MagicMock(api_key=None)) == valid_api_key


def test_get_api_key_with_argument():
    args = MagicMock(api_key="argument_api_key")
    assert get_api_key(args) == "argument_api_key"


def test_get_api_key_missing():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError):
            get_api_key(MagicMock(api_key=None))


# Test fetch_location_by_city_state function
@patch('geoloc_util.requests.get')
def test_fetch_location_by_city_state_success(mock_get, valid_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_city_state_response
    result = fetch_location_by_city_state("Madison, WI", valid_api_key)
    assert result == mock_city_state_response[0]


@patch('geoloc_util.requests.get')
def test_fetch_location_by_city_state_failure(mock_get, valid_api_key):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = []
    with pytest.raises(ValueError):
        fetch_location_by_city_state("Madison, WI", valid_api_key)


# Test fetch_location_by_zip function
@patch('geoloc_util.requests.get')
def test_fetch_location_by_zip_success(mock_get, valid_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_zip_response
    result = fetch_location_by_zip("12345", valid_api_key)
    assert result == mock_zip_response


@patch('geoloc_util.requests.get')
def test_fetch_location_by_zip_failure(mock_get, valid_api_key):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {}
    with pytest.raises(ValueError):
        fetch_location_by_zip("12345", valid_api_key)


# Test get_location_data function
@patch('geoloc_util.fetch_location_by_city_state')
@patch('geoloc_util.fetch_location_by_zip')
def test_get_location_data(mock_fetch_zip, mock_fetch_city_state, valid_api_key, mock_args):
    mock_fetch_city_state.return_value = mock_city_state_response[0]
    mock_fetch_zip.return_value = mock_zip_response
    results = get_location_data(valid_api_key, mock_args.locations)
    assert len(results) == 2
    assert results[0]["input"] == "Madison, WI"
    assert results[0]["latitude"] == 43.0731
    assert results[0]["longitude"] == -89.4012
    assert results[1]["input"] == "12345"
    assert results[1]["latitude"] == 40.7128
    assert results[1]["longitude"] == -74.0060


# Test exception handling in get_location_data
@patch('geoloc_util.fetch_location_by_city_state')
@patch('geoloc_util.fetch_location_by_zip')
def test_get_location_data_with_errors(mock_fetch_zip, mock_fetch_city_state, valid_api_key, mock_args):
    mock_fetch_city_state.side_effect = ValueError("Could not retrieve location data for Madison, WI")
    mock_fetch_zip.return_value = mock_zip_response
    results = get_location_data(valid_api_key, mock_args.locations)
    assert len(results) == 1  # Only the zip code data should be returned
    assert results[0]["input"] == "12345"
