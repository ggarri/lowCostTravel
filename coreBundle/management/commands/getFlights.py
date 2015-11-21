import datetime
import sys

from django.core.management.base import BaseCommand, CommandError
from dateutil.rrule import rrule, DAILY
from coreBundle.management.MyThread import *
from coreBundle.bussiness.CrawlBusiness import CrawlBusiness
from coreBundle.bussiness.TheadBussiness import TheadBussiness
from coreBundle.crawlers import EdreamsCrawler


class Command(BaseCommand):

    args = '<country_orig country_dest date_from date_to>'
    help = 'Closes the specified poll for voting'

    def __init__(self):
        _crawler = EdreamsCrawler()
        self.crawler_bc = CrawlBusiness(_crawler)
        self.thead_bc = TheadBussiness(self.crawler_bc, 2, 2)
        self.thead_bc.run()

    def handle(self, *args, **options):

        if len(args) < 4:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)

        date_from = datetime.datetime.strptime(args[2], "%d/%m/%Y").date()
        date_to = datetime.datetime.strptime(args[3], "%d/%m/%Y").date()

        self.one_way_trip_finder(args[0], args[1], date_from, date_to)
        self.one_way_trip_finder(args[1], args[0], date_from, date_to)
        self.round_trip_finder(args[0], args[1], date_from, date_to)

    def round_trip_finder(self, code_from, code_to, date_from, date_to):
        cheapest_flight_go = self.crawler_bc.get_list_cheapest_flight(code_from, code_to)
        cheapest_flight_back = self.crawler_bc.get_list_cheapest_flight(code_to, code_from)

        for cheap_flight_go in cheapest_flight_go:
            for cheap_flight_back in cheapest_flight_back:
                if cheap_flight_go.date_in.strftime('%Y%m%d') < cheap_flight_back.date_in.strftime('%Y%m%d'):
                    self.thead_bc.push_work({
                        'orig': cheap_flight_go.get_airport_in().code
                        , 'dest': cheap_flight_back.get_airport_in().code
                        , 'tripType': 'ROUND_TRIP'
                        , 'dateIn': cheap_flight_go.date_in.strftime("%d/%m/%Y")
                        , 'dateOut': cheap_flight_back.date_in.strftime("%d/%m/%Y")
                    })

    def one_way_trip_finder(self, orig, dest, date_from, date_to):

        for dt in rrule(DAILY, dtstart=date_from, until=date_to):
            self.thead_bc.push_work({
                'orig': orig
                , 'dest': dest
                , 'tripType': 'ONE_WAY'
                , 'dateIn': dt.strftime("%d/%m/%Y")
                , 'dateOut': None
            })