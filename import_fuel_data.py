
#<---Import fuel data from a CSV file into the database using a Django management command--->

import os
from django.conf import settings
import pandas as pd
from django.core.management.base import BaseCommand
from api.models import FuelOptimization

class Command(BaseCommand):
    help='Import fuel data from a CSV file'

    def handle(self, *args, **kwargs):
        df=os.path.join(settings.BASE_DIR, 'api', 'fuel-prices-for-be-assessment.csv')
        df=pd.read_csv(df)
        for _, row in df.iterrows():
            FuelOptimization.objects.update_or_create(
                opis_truckstop_id=row['OPIS Truckstop ID'],
                defaults={
                    'truckstop_name': row['Truckstop Name'],
                    'address': row['Address'],
                    'city': row['City'],
                    'state': row['State'],
                    'rack_id': row['Rack ID'],
                    'retail_price': row['Retail Price']
                }
            )
        self.stdout.write(self.style.SUCCESS('Fuel data imported successfully.'))