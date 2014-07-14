from django.db import models
from crawlers.edreams import *
from django.db.models import Avg, Max, Min, Count

import itertools

import time

########################################################
##      FLIGHT ENTITY
########################################################

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

    @staticmethod
    def storeEdreamsFlightByCode(geoIdIn, geoIdOut, dateIn , dateOut = None, tripType = 'ONE_WAY'):
        flightsData = getEdreamCrawledFlights(tripType, geoIdIn, geoIdOut, None, None, dateIn, dateOut)
        print flightsData
        dateInConv = time.strptime(dateIn, "%d/%m/%Y")
        dateInFormated = time.strftime("%Y-%m-%d",dateInConv)

        if dateOut != None:
            dateOutConv = time.strptime(dateOut, "%d/%m/%Y")
            dateOutFormated = time.strftime("%Y-%m-%d",dateOutConv)
        else:
            dateOutFormated = None

        Flight.objects.filter(edreams_geoId_in = geoIdIn, edreams_geoId_out = geoIdOut
                                                            , trip_type = tripType, date_in = dateInFormated
                                                            , date_out = dateOutFormated).delete()

        if len(flightsData) == 0:
            flightObj = Flight(edreams_geoId_in = geoIdIn, edreams_geoId_out = geoIdOut
                                                            , trip_type = tripType, date_in = dateInFormated
                                                            , date_out = dateOutFormated, price=-1)
        else:
            for flightData in flightsData:
                print flightData
                flightObj = Flight(edreams_geoId_in = geoIdIn, edreams_geoId_out = geoIdOut
                                                                , trip_type = tripType, date_in = dateInFormated
                                                                , date_out = dateOutFormated)

                flightObj.duration_in = flightData['durationIn']
                flightObj.duration_out = flightData['durationOut']
                flightObj.stops_in = flightData['stopsIn']
                flightObj.stops_out = flightData['stopsOut']
                flightObj.price = flightData['price']
                flightObj.save()

        flightObj.save()

    @staticmethod
    def storeEdreamsFlightBetweenCountries(country_code_in, country_code_out, date_in, date_out = None, only_main = True):
        countryIn = Country.objects.get(code=country_code_in)
        countryOut = Country.objects.get(code=country_code_out)
        airportsIn = Airport.objects.filter(country=countryIn, is_main=only_main)
        airportsOut = Airport.objects.filter(country=countryOut, is_main=only_main)

        if date_out == None:
            tripType = 'ONE_WAY'
        else:
            tripType = 'ROUND_TRIP'

        for airportIn in airportsIn:
            for airportOut in airportsOut:
                Flight.storeEdreamsFlightByCode(airportIn.edreams_geoId, airportOut.edreams_geoId
                                                 , date_in, date_out, tripType)

    @staticmethod
    def getListCheapestFlight(codeIn, codeOut, dateFrom, dateTo, limit=10):

        if len(codeIn) == 2:
            countryIn = Country.objects.get(code=codeIn)
            aAirportsIn = Airport.objects.filter(country=countryIn)
        else:
            aAirportsIn = Airport.objects.filter(code=codeIn)

        if len(codeOut) == 2:
            countryOut = Country.objects.get(code=codeOut)
            aAirportsOut = Airport.objects.filter(country=countryOut)
        else:
            aAirportsOut = Airport.objects.filter(code=codeOut)



        aFlightsGo = Flight.objects.filter(edreams_geoId_in__in = aAirportsIn.values_list('edreams_geoId', flat=True),
                              edreams_geoId_out__in = aAirportsOut.values_list('edreams_geoId', flat=True)
                              ).exclude(price=-1).order_by('price')[:10]
        # .annotate(Count('edreams_geoId_in'), Count('edreams_geoId_out'))

        return aFlightsGo



########################################################
##      COUNTRY ENTITY
########################################################


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


########################################################
##      AIRPORT ENTITY
########################################################

class Airport(models.Model):

    country = models.ForeignKey(Country)
    edreams_geoId = models.IntegerField(unique=True)
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    is_main = models.BooleanField(default=False)

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
                                                         , code=dataAirport['code'])
            newAiportObj.city = dataAirport['city']
            newAiportObj.save()

    @staticmethod
    def storeEdreamsCities():
        countries = Country.objects.all()
        for country in countries:
               Airport.storeEdreamsCitiesByCountry(country)

    @staticmethod
    def resetAirportIsMainByCountryCode(country_code):
        country = Country.objects.get(code=country_code)
        Airport.objects.filter(country=country).update(is_main=True)


    def getBestConexionAirports(self, country_code_out):
        oCountryOut = Country.objects.get(code=country_code_out)
        aAirportOut = Airport.objects.filter(country=oCountryOut, is_main=True)

        # Calculate global avarage prices
        aAllFlights = Flight.objects.filter(edreams_geoId_in=self.edreams_geoId
                                       , edreams_geoId_out__in=aAirportOut.values_list('edreams_geoId')) \
                      | Flight.objects.filter(edreams_geoId_out=self.edreams_geoId
                                       , edreams_geoId_in__in=aAirportOut.values_list('edreams_geoId'))

        aAllFlightPrice = set(aAllFlights.values_list('price', flat=True))
        aFlightDateRange = set(aAllFlights.values_list('date_in'))

        if 0 == len(aAllFlightPrice):
            fGlobalAvaragePrice = None
        else:
            fGlobalAvaragePrice = reduce(lambda x, y: x + y, aAllFlightPrice) / len(aAllFlightPrice)
            print "Global avarage price %f with %d days crawled" % (fGlobalAvaragePrice, len(aFlightDateRange))

        # Get the list of airport which has price lower than global avarage
        aBestAirportGeoId = []
        for oAirporOut in aAirportOut:
            aFlightOutList = Flight.objects.filter(edreams_geoId_in=self.edreams_geoId
                                       , edreams_geoId_out=oAirporOut.edreams_geoId) \
                      | Flight.objects.filter(edreams_geoId_out=self.edreams_geoId
                                       , edreams_geoId_in=oAirporOut.edreams_geoId)

            aFlightPrice = set(aFlightOutList.values_list('price', flat=True))

            # It wasn't crawled it, then give it a chance ;)
            if 0 != len(aFlightPrice):
                fPriceAirportAvarage = reduce(lambda x, y: x + y, aFlightPrice) / len(aFlightPrice)
                # print "Airport %s avarage price %f" % (oAirporOut.city, fPriceAirportAvarage)
            else:
                fPriceAirportAvarage = -1

            # If there is not previous experience, or avarage price is lower or there isn't more than 1 day crawled
            # print fPriceAirportAvarage < fGlobalAvaragePrice, fPriceAirportAvarage, fGlobalAvaragePrice
            if None == fGlobalAvaragePrice or (fPriceAirportAvarage < fGlobalAvaragePrice and fPriceAirportAvarage > 0) \
                    or len(aFlightDateRange) < 3:
                aBestAirportGeoId.append(oAirporOut.edreams_geoId)

        return Airport.objects.filter(edreams_geoId__in=aBestAirportGeoId)







