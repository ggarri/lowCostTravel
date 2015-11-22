__author__ = 'ggarrido'

import Queue
import threading
import time
from coreBundle.models.Airport import Airport
from coreBundle.models.Country import Country
from coreBundle.bussiness.CrawlBusiness import CrawlBusiness


class TheadBussiness():

    consumers = []
    nc = 10
    consumer_queue = Queue.Queue(0)

    producers = []
    np = 2
    producer_queue = Queue.Queue(0)

    _lock = threading.Condition(threading.Lock())
    _cond = threading.Condition(_lock)

    _lock2 = threading.Condition(threading.Lock())
    _cond2 = threading.Condition(_lock2)

    def __init__(self, crawler_bc, n_consumer, n_producer):
        """
        :param crawler_bc: CrawlBusiness
        :param n_consumer: int
        :param n_producer: int
        """
        self.nc = n_consumer
        self.np = n_producer
        self.crawl_bc = crawler_bc

    def run(self):
        for tId in range(0, self.nConsumer):
            t = Consumer(tId, self._lock, self._cond, self.consumer_queue)
            t.set_up(self.crawl_bc)
            t.start()
            self.consumers.append(t)

        for tId in range(0, self.nProducer):
            t = Producer(tId, self._lock2, self._cond2, self.producer_queue, self.consumer_queue)
            t.set_up(self.crawl_bc)
            t.start()
            self.producers.append(t)

    def push_work(self, data):
        self.producer_queue.put(data)


class Consumer(threading.Thread):
    
    """
    :type crawler: CrawlBusiness
    """
    crawler = None

    def __init__(self, thead_id, lock, cond, q):
        threading.Thread.__init__(self)
        self.thead_id = thead_id
        self.name = 'Consumer-'+str(self.thead_id)
        self.q = q
        self.lock = lock
        self.cond = cond

    def set_up(self, crawler_bc):
        self.crawler = crawler_bc

    def run(self):
        print "Starting " + self.name
        while True:
            self.consume()
        print "Exiting " + self.name

    def consume(self):
        self.cond.acquire()
        while self.q.empty():
            print "%s: Waiting for work to do." % self.name
            time.sleep(1)
            # self.cond.wait()
        job = self.q.get()
        self.cond.release()

        print "%s: Running flight [%s>%s] at %s" % (self.name, job['airportIn'], job['airportOut'],
                                                    job['dateInFormatted'])

        self.crawler.store_flights_between_geo_id(job['airportIn'], job['airportOut'],
                                                  job['dateInFormatted'], job['dateOutFormatted'])


class Producer (threading.Thread):

    """
    :type crawler: CrawlBusiness
    """
    crawler = None
    
    def __init__(self, thead_id, lock, cond, q, q2):
        threading.Thread.__init__(self)
        self.thead_id = thead_id
        self.name = 'Productor-'+str(self.thead_id)
        self.q = q
        self.q2 = q2
        self.lock = lock
        self.cond = cond

    def set_up(self, crawler_bc):
        self.crawler = crawler_bc

    def run(self):
        print "Starting " + self.name
        while True:
            self.produce()
        print "Exiting " + self.name

    def produce(self):
        self.cond.acquire()
        while self.q.empty():
            print "%s: Waiting for work to do." % self.name
            time.sleep(1)
            # self.cond.wait()
        job = self.q.get()
        self.cond.release()

        print "%s: Pushing [%s>%s] at %s - %s" % (self.name, job['orig'], job['dest'], job['dateIn'], job['dateOut'])
        self._push_flight_data(job['orig'], job['dest'], job['tripType'], job['dateIn'], job['dateOut'])

    def _push_flight_data(self, orig, dest, trip_type, date_from, date_to):
        if len(orig) == 2:
            country_from = Country.objects.get(code=orig)
            airpots_from = Airport.objects.filter(country=country_from, is_main=True)
        else:
            airpots_from = Airport.objects.filter(code=orig)

        for airportIn in airpots_from:
            # In case of 2 lenght, it is a country code otherwise it is an aiport
            if len(dest) == 2:
                airports_to = self.crawler.get_best_conexion(airportIn, dest)
            else:
                airports_to = Airport.objects.filter(code=dest)

            for airportOut in airports_to:
                print "%s: Pushing [%s>%s] at %s" % (self.name, airportIn.code, airportOut.code, date_from)
                self.q2.put({
                    'dateInFormatted': date_from,
                    'dateOutFormatted': date_to,
                    'tripType': trip_type,
                    'airportIn': airportIn.code,
                    'airportOut': airportOut.code
                })