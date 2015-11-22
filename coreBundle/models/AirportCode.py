__author__ = 'ggarrido'

from coreBundle.models.Airport import Airport
from django.db import models


class AirportCode(models.Model):
    airport = models.ForeignKey(Airport)
    edreams_geoId = models.IntegerField(unique=True)