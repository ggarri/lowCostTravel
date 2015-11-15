__author__ = 'ggarrido'

from django.db import models
from coreBundle.models.Country import Country


class Airport(models.Model):
    country = models.ForeignKey(Country)
    edreams_geoId = models.IntegerField(unique=True)
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    is_main = models.BooleanField(default=False)

    # GeoId of crawler we are working on
    geo_id = None

    def __init__(self):
        # TODO Get enviroment crawltype to set this value depending on it
        self.geo_id = self.edreams_geoId