__author__ = 'ggarrido'

from django.db import models
from coreBundle.models.Country import Country


class Airport(models.Model):
    country = models.ForeignKey(Country)
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    is_main = models.BooleanField(default=False)