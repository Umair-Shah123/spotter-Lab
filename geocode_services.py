from decouple import config

from opencage.geocoder import OpenCageGeocode

class GeocodeService:
   @staticmethod
   def get_coordinates(address):
        geocoder = OpenCageGeocode(config('OPENCAGE_API_KEY'))
        
    
        results = geocoder.geocode(address)
        if results and len(results) > 0:
            return {
                'lat': results[0]['geometry']['lat'],
                'lng': results[0]['geometry']['lng']
            }
        return None