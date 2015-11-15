__author__ = 'ggarrido'

from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)