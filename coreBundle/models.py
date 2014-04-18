from django.db import models
from crawlers.edreams import *

import itertools

class Country(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)

    @staticmethod
    def storeEdreamsCountryCodeByLetter(letter):
        codeNames = getEdreamCrawledCountries(letter)
        print codeNames
        for codeName in codeNames:
            print codeName
            countryObj, isNew = Country.objects.get_or_create(code=codeName['code'])
            countryObj.name = codeName['name']
            countryObj.save()

    @staticmethod
    def storeEdreamsCountryCode():
        for letter in list(map(chr, range(97, 123))):
            Country.storeEdreamsCountryCodeByLetter(letter)



class Airport(models.Model):

    country = models.ForeignKey(Country)
    edreams_geoId = models.IntegerField(unique=True)
    edreams_code = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def storeEdreamsCitiesByCountryCode(country_code):
        country = Country.objects.get(code=country_code)
        Airport.storeEdreamsCitiesByCountry(country)

    @staticmethod
    def storeEdreamsCitiesByCountry(country):
        dataAirports = getEdreamCrawledAiports(country.code)
        for dataAirport in dataAirports:
            print dataAirport
            newAiportObj, isNew = Airport.objects.get_or_create(edreams_geoId=dataAirport['geoId'], country=country
                                                         , edreams_code=dataAirport['code'])
            newAiportObj.city = dataAirport['city']
            newAiportObj.save()

    @staticmethod
    def storeEdreamsCities():
        countries = Country.objects.all()
        for country in countries:
               Airport.storeEdreamsCitiesByCountry(country)


