from django.core.management.base import BaseCommand
from api.models import FuelOptimization
from opencage.geocoder import OpenCageGeocode
import time
import os

class Command(BaseCommand):
    help = 'Geocode addresses and update latitude and longitude in the database'

    def handle(self, *args, **kwargs):
        api_key = os.getenv('OPENCAGE_API_KEY')
        geocoder = OpenCageGeocode(api_key)

        fuel_stops = FuelOptimization.objects.filter(latitude__isnull=True, longitude__isnull=True)
        for stop in fuel_stops:
            query = f"{stop.address}, {stop.city}, {stop.state}"
            try:
                results = geocoder.geocode(query)
                if results and len(results) > 0:
                    stop.latitude = results[0]['geometry']['lat']
                    stop.longitude = results[0]['geometry']['lng']
                    stop.save()
                    self.stdout.write(self.style.SUCCESS(f"Geocoded: {query}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No results for: {query}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error geocoding {query}: {e}"))
            time.sleep(1)  