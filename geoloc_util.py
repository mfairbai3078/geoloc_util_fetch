#!/usr/bin/env python3
import os
import requests
import argparse
import logging
from typing import List, Dict

__author__ = "Matthew Fairbairn"
__version__ = "1.0.0"
__maintainer__ = "Matthew Fairbairn"
__email__ = "fairbairn.matthew@gmail.com"
__status__ = "Demo"

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
API_URL_CITY_STATE = "http://api.openweathermap.org/geo/1.0/direct"
API_URL_ZIP_CODE = "http://api.openweathermap.org/geo/1.0/zip"


def get_api_key(args) -> str:
    """
    Retrieve the OpenWeather API key from environment variables.
    """
    if args.api_key:
        api_key = args.api_key
    else:
        api_key = os.getenv('API_KEY')
    if not api_key:
        logging.error("API_KEY environment variable not found or not specified on commandline.")
        raise EnvironmentError("API_KEY not found in environment variables or not specified on commandline.")
    return api_key


def fetch_location_by_city_state(city_state: str, api_key: str) -> Dict:
    """
    Fetch geolocation data using city and state.

    :param city_state: The city and state input (e.g., "Madison, WI")
    :param api_key: The API key for the OpenWeather API
    :return: A dictionary with geolocation data
    """
    if len(city_state.split(',')) == 3:
        country_code = city_state.split(',')[-1]
    else:
        country_code = "US"
    city, state = city_state.split(",")[:2]
    params = {
        "q": f"{city},{state},{country_code}",
        "appid": api_key,
        "limit": 1  # Return only the first result
    }
    response = requests.get(API_URL_CITY_STATE, params=params)

    if response.status_code == 200 and response.json():
        return response.json()[0]
    else:
        logging.error(f"Error fetching data for {city_state}: {response.text}")
        raise ValueError(f"Could not retrieve location data for {city_state}.")


def fetch_location_by_zip(zip_code: str, api_key: str) -> Dict:
    """
    Fetch geolocation data using zip code.

    :param zip_code: The zip code input (e.g., "12345")
    :param api_key: The API key for the OpenWeather API
    :return: A dictionary with geolocation data
    """
    if len(zip_code.split(',')) == 2:
        country_code=zip_code.split(',')[-1]
        zip = zip_code.split(',')[0]
    else:
        country_code = "US"
        zip = zip_code

    params = {
        "zip": f"{zip},{country_code}",
        "appid": api_key
    }
    response = requests.get(API_URL_ZIP_CODE, params=params)

    if response.status_code == 200 and response.json():
        return response.json()
    else:
        logging.error(f"Error fetching data for {zip_code}: {response.text}")
        raise ValueError(f"Could not retrieve location data for {zip_code}.")


def get_location_data(api_key, locations: List[str]) -> List[Dict]:
    """
    Get geolocation data for multiple locations.

    :param api_key:  The API key for the OpenWeather API
    :param locations: List of location strings (e.g., ["Madison, WI", "12345"])
    :return: List of dictionaries with geolocation data
    """

    results = []

    for location in locations:
        try:
            if location.split(',')[0].isalpha():  # City/State input
                data = fetch_location_by_city_state(location, api_key)
            else:  # Zip code input
                data = fetch_location_by_zip(location, api_key)

            results.append({
                "input": location,
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "place_name": data.get("name", data.get("zip")),
            })
        except ValueError as e:
            logging.warning(f"Skipping location {location}: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch geolocation data for cities/states or zip codes.")
    parser.add_argument("--api-key", help="API Key for the OpenWeather Geocoding API", default=None)
    parser.add_argument("--locations", action="store_true", help="List of city/state or zip code locations", required=False)
    parser.add_argument("locations", nargs="+", help="List of city/state or zip codes (e.g., 'Madison, WI' '12345').")
    args = parser.parse_args()

    api_key = get_api_key(args)
    results = get_location_data(api_key, args.locations)
    for result in results:
        print("-" * 80)
        print(f"Input: {result['input']}")
        print(f"Latitude: {result['latitude']}")
        print(f"Longitude: {result['longitude']}")
        print(f"Place Name: {result['place_name']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
