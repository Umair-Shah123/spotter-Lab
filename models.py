from django.db import models

# Create your models here.
class FuelOptimization(models.Model):
    
    opis_truckstop_id=models.IntegerField(unique=True)
    truckstop_name=models.CharField(max_length=255  )
    address=models.CharField(max_length=200  )
    city=models.CharField(max_length=200  )
    state=models.CharField(max_length=200  )
    rack_id=models.IntegerField()
    retail_price=models.DecimalField(max_digits=10, decimal_places=6)
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.truckstop_name}-{self.city}, {self.state}"