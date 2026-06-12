from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RouteSerializer
from .services.geocode_services import GeocodeService
from .services.routing_services import RoutingService
from rest_framework.permissions import AllowAny
from .services.fuel_services import FuelService
from .services.optimizers_services import FuelCostCalculator

# Create your views here.
class RouteOPTIMIZATION(APIView):
    permission_classes = [AllowAny]  
    def post(self,request):
        serializer = RouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        origin = serializer.validated_data['origin']
        destination = serializer.validated_data['destination']

        start_coords = GeocodeService.get_coordinates(origin)
        end_coords = GeocodeService.get_coordinates(destination)

        rouete_data=RoutingService.get_route(start_coords, end_coords)
        summary = rouete_data['features'][0]['properties']['summary']
        
        distance_miles = round(summary['distance'] * 0.000621371)  # Convert meters to miles
        nearby_stops=  FuelService.find_fuel_stops_along_route(rouete_data['features'][0]['geometry'])
        trip_result=FuelCostCalculator.calculate_fuel_cost(nearby_stops, distance_miles)

        return Response({
            'distance':round(distance_miles, 2) , # Convert meters to miles
            'duration':round( summary['duration']/3600,2) , # Convert seconds to hours
            'fuel_stops': trip_result['fuel_stops'],
             'total_fuel_cost': trip_result['total_fuel_cost'],
             'route_geometry': rouete_data['features'][0]['geometry']
        },
        
        status=200
    )