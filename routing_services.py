import requests
from decouple import config

class RoutingService:
    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
    @staticmethod
    def get_route(origin, destination):
        api_key = config('OPENROUTE_SERVICE_KEY')
        headers = {
            'Authorization': config('OPENROUTE_SERVICE_KEY'),
            'Content-Type': 'application/json'
        } 
        data = {
            "coordinates": [
                [origin['lng'], origin['lat']],
                [destination['lng'], destination['lat']]
            ]
        }
        response = requests.post(RoutingService.BASE_URL, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching route: {response.status_code} - {response.text}")

    def geocode(self, address):
        params = {
            'q': address,
            'key': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['geometry']
        return None