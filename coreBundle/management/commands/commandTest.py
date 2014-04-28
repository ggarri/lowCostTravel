from django.core.management.base import BaseCommand, CommandError
from datetime import date
from dateutil.rrule import rrule, DAILY
import datetime

import sys
import getopt
from coreBundle.torAnonymous.tor import *
from coreBundle.models import *

class Command(BaseCommand):

    args = '<country_orig country_dest date_from date_to>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if len(args) < 4:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)

        self.storePeriod(args[0], args[1], args[2], args[3])
    # Country.objects.get(code=argv[0])
    # Flight.storeEdreamsFlightBetweenCountries()

    def storePeriod(self, orig, dest, _from, _to):

        dateFrom = datetime.datetime.strptime(_from, "%d/%m/%Y").date()
        dateTo = datetime.datetime.strptime(_to, "%d/%m/%Y").date()

        for dt in rrule(DAILY, dtstart=dateFrom, until=dateTo):
            Flight.storeEdreamsFlightBetweenCountries(country_code_in = orig
                                                      , country_code_out = dest
                                                      , date_in = dt.strftime("%d/%m/%Y")
            )