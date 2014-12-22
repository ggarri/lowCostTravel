import datetime
import sys

from django.core.management.base import BaseCommand, CommandError
from dateutil.rrule import rrule, DAILY
from coreBundle.management.MyThread import *

class Command(BaseCommand):

    args = '<country_orig country_dest date_from date_to>'
    help = 'Closes the specified poll for voting'

    consumerList = []
    nConsumer = 10
    consumerQueue = Queue.Queue(0)

    producerList = []
    nProducer = 2
    producerQueue = Queue.Queue(0)

    _lock = threading.Condition(threading.Lock())
    _cond = threading.Condition(_lock)

    _lock2 = threading.Condition(threading.Lock())
    _cond2 = threading.Condition(_lock2)

    def handle(self, *args, **options):

        if len(args) < 4:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)

        dateFrom = datetime.datetime.strptime(args[2], "%d/%m/%Y").date()
        dateTo = datetime.datetime.strptime(args[3], "%d/%m/%Y").date()

        self.initThreads()

        self.storePeriod(args[0], args[1], dateFrom, dateTo)
        self.storePeriod(args[1], args[0], dateFrom, dateTo)
        self.roundTripPeriod(args[0], args[1], dateFrom, dateTo)

    def initThreads(self):
        for tId in range(0, self.nConsumer):
            t = consumer(tId, self._lock, self._cond, self.consumerQueue)
            t.start()
            self.consumerList.append(t)

        for tId in range(0, self.nProducer):
            t = producer(tId, self._lock2, self._cond2, self.producerQueue, self.consumerQueue)
            t.start()
            self.producerList.append(t)

    def roundTripPeriod(self, orig, dest, dateFrom, dateTo):
        aCheapestFlightGo = Flight.getListCheapestFlight(orig, dest, dateFrom, dateTo)
        aCheapestFlightBack = Flight.getListCheapestFlight(dest, orig, dateFrom, dateTo)
        for oCheapestFlightGo in aCheapestFlightGo:
            for oCheapestFlightBack in aCheapestFlightBack:
                if oCheapestFlightGo.date_in.strftime('%Y%m%d') < oCheapestFlightBack.date_in.strftime('%Y%m%d'):
                    Flight.storeEdreamsFlightByCode(oCheapestFlightGo.edreams_geoId_in,
                                                            oCheapestFlightBack.edreams_geoId_in,
                                                            oCheapestFlightGo.date_in.strftime("%d/%m/%Y"),
                                                            oCheapestFlightBack.date_in.strftime("%d/%m/%Y"),
                                                            'ROUND_TRIP')



    def storePeriod(self, orig, dest, dateFrom, dateTo):

        for dt in rrule(DAILY, dtstart=dateFrom, until=dateTo):
            self.producerQueue.put({
                'orig': orig
                , 'dest': dest
                , 'tripType': 'ONE_WAY'
                , 'dateIn': dt.strftime("%d/%m/%Y")
                , 'dateOut': None
            })