# Geolocation Utility

This command-line utility fetches geographical information (latitude, longitude, place name, etc.) based on city/state or zip code inputs using the OpenWeather Geocoding API. The tool can process multiple locations at once, making it easy to retrieve geolocation data for various locations.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [FAQ](#FAQ)
 
## Features

- Supports input for city/state combinations (e.g., "Madison, WI") or zip codes (e.g., "10001").
- Fetches and displays latitude, longitude, and place names using the OpenWeatherMap Geocoding API.
- Handles multiple location queries at once.
- Designed to be easily configurable with an API key passed via command line or environment variable.

## Requirements

- Python 3.7+
- `requests` library
- `pytest` (for running tests)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mfairbai3078/geoloc_util_fetch.git
   cd geoloc_util_fetch


2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can run the script directly from the command line. Provide the locations as arguments and optionally specify an API key:

```bash
python geoloc-util.py "Madison, WI" "12345" --api-key YOUR_API_KEY
```
You can also specify the API key via the command line:

```bash
python geoloc_util.py --locations "Chicago, IL" "90210" --api-key your_api_key
```

Alternatively, you can set the API key as an environment variable:

```bash
export API_KEY="your_api_key"
python geoloc_util.py --locations "Austin, TX" "12345"
```

## Configuration
The utility expects the OpenWeatherMap API key to be passed either through, it is not provided here as it would be considered a security risk:

The --api-key command-line argument.
The API_KEY environment variable.

## Example Output

```yaml
Location: Madison, WI
  Latitude: 43.0731
  Longitude: -89.4012
  Place Name: Madison

Location: 10001
  Latitude: 40.7128
  Longitude: -74.0060
  Place Name: New York
```
## Running Tests
Unit tests are written using pytest. To run the tests:

```bash
pytest test_geoloc_util.py
```

The tests include mock responses for both city/state and zip code inputs.

Configuration
The utility expects the OpenWeatherMap API key to be passed either through:

The --api-key command-line argument.
The API_KEY environment variable.

## Project Structure
```plaintext
geoloc_util_fetch/
│
├── geoloc_util.py            # Main script
├── test_geoloc_util.py       # Pytest test cases
├── requirements.txt          # Python dependencies
└── README.md                 # This readme file
```


## FAQ

How can I get an API key?

You can obtain an API key by signing up here https://home.openweathermap.org/users/sign_up
