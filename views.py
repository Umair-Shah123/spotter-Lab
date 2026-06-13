from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RouteSerializer
from .services.geocode_services import GeocodeService
from .services.routing_services import RoutingService
from rest_framework.permissions import AllowAny
from .services.fuel_services import FuelService
from .services.optimizers_services import FuelCostCalculator
from rest_framework import status

class RouteOPTIMIZATION(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        origin = serializer.validated_data['origin']
        destination = serializer.validated_data['destination']

        start_coords = GeocodeService.get_coordinates(origin)
        end_coords = GeocodeService.get_coordinates(destination)

        print("START:", start_coords)
        print("END:", end_coords)

        if not start_coords or not end_coords:
            return Response({"error": "Geocoding failed"}, status=400)

        route_data = RoutingService.get_route(start_coords, end_coords)

        if not route_data or 'routes' not in route_data:
            return Response({
                "error": "Routing API failed",
                "details": route_data
            }, status=400)

        try:
            route = route_data['routes'][0]
            leg = route['legs'][0]

            distance_miles = leg['distance'] * 0.000621371
            geometry = route['geometry']

            print("GEOMETRY:", geometry)

            nearby_stops = FuelService.find_fuel_stops_along_route(geometry)

            print("STOPS:", nearby_stops)

            trip_result = FuelCostCalculator.calculate_fuel_cost(
                nearby_stops,
                distance_miles
            )

        except Exception as e:
            return Response({
                "error": "Pipeline crashed",
                "message": str(e)
            }, status=500)

        return Response({
            "distance": round(distance_miles, 2),
            "duration": round(leg['duration'] / 3600, 2),
            "fuel_stops": trip_result['fuel_stops'],
            "total_fuel_cost": trip_result['total_cost'],
            "route_geometry": geometry
        }, status=200)



















