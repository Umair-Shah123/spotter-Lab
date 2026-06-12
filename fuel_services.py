from shapely.geometry import Point, LineString
from api.models import FuelOptimization

class FuelService:
    @staticmethod
    def find_fuel_stops_along_route(route):
        route_coord=route_geometry(["coordinates"])
        route_line=LineString(route_coord)
        nearest_stops=[]
        stations=FuelOptimization.objects.exclude(latitude__isnull=True, longitude__isnull=True)

        for station in stations:
            station_point=Point(station.longitude, station.latitude)
            distance=route_line.distance(station_point)
            if distance < 0.01:
                nearest_stops.append({
                    'id': station.id,
                    'name': station.truckstop_name,
                    'address': station.address,
                    'city': station.city,
                    'state': station.state,
                    'rack_id': station.rack_id,
                    'retail_price': station.retail_price,
                    'latitude': station.latitude,
                    'longitude': station.longitude,
                    'distance_to_route': distance
                })
        return nearest_stops
