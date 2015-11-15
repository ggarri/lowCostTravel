__author__ = 'ggarrido'

from django.db import models
from coreBundle.models import Airport


class Flight(models.Model):
    FLIGHT_MODE = (
        ('ONE_WAY', 'one way'),
        ('ROUND_TRIP', 'round_trip')
    )

    edreams_geoId_in = models.IntegerField(blank=True, null=True)
    edreams_geoId_out = models.IntegerField(blank=True, null=True)
    price = models.FloatField(null=True)
    duration_in = models.CharField(max_length=10, blank=True, null=True)
    duration_out = models.CharField(max_length=10)
    stops_in = models.IntegerField(blank=True, null=True)
    stops_out = models.IntegerField(null=True)
    trip_type = models.CharField(max_length=10, choices=FLIGHT_MODE)
    date_in = models.DateTimeField()
    date_out = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def get_airport_in(self):
        return Airport.objects.filter(edreams_geoId=self.edreams_geoId_in)[0]

    def get_airport_out(self):
        return Airport.objects.filter(edreams_geoId=self.edreams_geoId_out)[0]