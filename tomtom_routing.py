import requests

API_KEY = "c3CGES0DiyRgtIPAqdqAxi3lIspyCr9U"

def get_route(locations):
    coord_str = ':'.join([f"{lat},{lon}" for lat, lon in locations])
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{coord_str}/json"
    params = {
        "key": API_KEY,
        "computeBestOrder": "true",
        "routeType": "fastest",
        "traffic": "true",
        "travelMode": "car"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        route = data["routes"][0]
        points = route["legs"][0]["points"]
        summary = route["summary"]
        return summary, [(pt["latitude"], pt["longitude"]) for pt in points]
    else:
        print("Error:", response.text)
        return None, None
