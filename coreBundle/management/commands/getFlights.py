from django.core.management.base import BaseCommand, CommandError
from datetime import date
from dateutil.rrule import rrule, DAILY
import datetime

import sys
from coreBundle.models import *

class Command(BaseCommand):

    args = '<country_orig country_dest date_from date_to>'

    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if len(args) < 4:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)

        dateFrom = datetime.datetime.strptime(args[2], "%d/%m/%Y").date()
        dateTo = datetime.datetime.strptime(args[3], "%d/%m/%Y").date()

        # self.roundTripPeriod(args[0], args[1], dateFrom, dateTo)
        self.storePeriod(args[0], args[1], dateFrom, dateTo)

    def roundTripPeriod(self, orig, dest, dateFrom, dateTo):
        countryIn = Country.objects.get(code=orig)
        countryOut = Country.objects.get(code=dest)
        aCheapestFlightGo = Flight.getListCheapestFlight(countryIn, countryOut, dateFrom, dateTo)
        aCheapestFlightBack = Flight.getListCheapestFlight(countryOut, countryIn, dateFrom, dateTo)

        iMin = 9999999999999
        for oCheapestFlightGo in aCheapestFlightGo:
            for oCheapestFlightBack in aCheapestFlightBack:
                if oCheapestFlightGo.date_in.strftime('%Y%m%d') < oCheapestFlightBack.date_in.strftime('%Y%m%d'):
                    if  (oCheapestFlightGo.price + oCheapestFlightBack.price) < iMin:
                        iMin = oCheapestFlightGo.price + oCheapestFlightBack.price
                        print iMin, oCheapestFlightGo.edreams_geoId_in,oCheapestFlightBack.edreams_geoId_in, oCheapestFlightGo.date_in, oCheapestFlightBack.date_in
                        Flight.storeEdreamsFlightByCode(oCheapestFlightGo.edreams_geoId_in,
                                                                oCheapestFlightBack.edreams_geoId_in,
                                                                oCheapestFlightGo.date_in.strftime("%d/%m/%Y"),
                                                                oCheapestFlightBack.date_in.strftime("%d/%m/%Y"),
                                                                'ROUND_TRIP')



    def storePeriod(self, orig, dest, dateFrom, dateTo):

        for dt in rrule(DAILY, dtstart=dateFrom, until=dateTo):
            countryIn = Country.objects.get(code=orig)
            airportsIn = Airport.objects.filter(country=countryIn, is_main=True)
            tripType = 'ONE_WAY'
            dateInFormatted = dt.strftime("%d/%m/%Y")

            for airportIn in airportsIn:
                airportsOut = airportIn.getBestConexionAirports(dest)
                for airportOut in airportsOut:
                    print "From %s to %s at %s" % (airportIn.code, airportOut.code, dateInFormatted)
                    Flight.storeEdreamsFlightByCode(airportIn.edreams_geoId, airportOut.edreams_geoId
                                                     , dateInFormatted, None, tripType)