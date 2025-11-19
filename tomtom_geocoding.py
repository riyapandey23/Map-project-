# tomtom_geocoding.py

import requests

API_KEY = "c3CGES0DiyRgtIPAqdqAxi3lIspyCr9U"

def get_coordinates(location_name):
    url = f"https://api.tomtom.com/search/2/geocode/{location_name}.json?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            position = data['results'][0].get('position')
            if position:
                return position.get('lat'), position.get('lon')
    return None

def reverse_geocode(lat, lon):
    url = f"https://api.tomtom.com/search/2/reverseGeocode/{lat},{lon}.json?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('addresses'):
            return data['addresses'][0]['address']
    return None
