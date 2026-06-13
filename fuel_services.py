from shapely import geometry
from shapely.geometry import Point, LineString
from api.models import FuelOptimization



class FuelService:
    @staticmethod
    def find_fuel_stops_along_route(geometry):

       
        if not isinstance(geometry, dict):
            raise ValueError(f"Invalid geometry type: {type(geometry)}")

        if 'coordinates' not in geometry:
            raise KeyError(f"'coordinates' missing in geometry: {geometry}")

        route_coords = geometry['coordinates']

        route_line = LineString(route_coords)

        nearest_stops = []
        stations = FuelOptimization.objects.exclude(
            latitude__isnull=True,
            longitude__isnull=True
        )

        for station in stations:
            station_point = Point(station.longitude, station.latitude)

            distance = route_line.distance(station_point)

            if distance < 0.01:
                nearest_stops.append({
                    'name': station.truckstop_name,
                    'city': station.city,
                    'state': station.state,
                    'price': float(station.retail_price),
                })

        return nearest_stops

