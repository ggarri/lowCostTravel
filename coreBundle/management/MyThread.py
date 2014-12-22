#!/usr/bin/python

import Queue
import threading
import time
from datetime import date
from coreBundle.models import *


class consumer (threading.Thread):

    def __init__(self, threadID, lock, cond, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'Consumer-'+str(self.threadID)
        self.q = q
        self.lock = lock
        self.cond = cond

    def run(self):
        print "Starting " + self.name
        while True:
            self.consume()
        print "Exiting " + self.name

    def consume(self):
        self.cond.acquire()
        while self.q.empty():
            print "%s: Waiting for work to do." % (self.name)
            time.sleep(1)
            # self.cond.wait()
        job = self.q.get()
        self.cond.release()

        print "%s: Running flight [%s>%s] at %s" % (self.name, job['codeIn'], job['codeOut'], job['dateInFormatted'])
        Flight.storeEdreamsFlightByCode(job['edreams_geoId'], job['edreams_geoOut']
                                        , job['dateInFormatted'], job['dateOutFormatted'], job['tripType'])


class producer (threading.Thread):

    def __init__(self, threadID, lock, cond, q, q2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'Productor-'+str(self.threadID)
        self.q = q
        self.q2 = q2
        self.lock = lock
        self.cond = cond

    def run(self):
        print "Starting " + self.name
        while True:
            self.produce()
        print "Exiting " + self.name

    def produce(self):
        self.cond.acquire()
        while self.q.empty():
            print "%s: Waiting for work to do." % (self.name)
            time.sleep(1)
            # self.cond.wait()
        job = self.q.get()
        self.cond.release()

        print "%s: Pushing [%s>%s] at %s" % (self.name, job['orig'], job['dest'], job['dateIn'])
        self._pushFlighData(job['orig'], job['dest'], job['tripType'], job['dateIn'], job['dateOut'])

    def _pushFlighData(self, orig, dest, tripType, dateIn, dateOut):
        if len(orig) == 2:
            countryIn = Country.objects.get(code=orig)
            airportsIn = Airport.objects.filter(country=countryIn, is_main=True)
        else:
            airportsIn = Airport.objects.filter(code=orig)

        for airportIn in airportsIn:
            if len(dest) == 2:
                airportsOut = airportIn.getBestConexionAirports(dest)
            else:
                airportsOut = Airport.objects.filter(code=dest)

            for airportOut in airportsOut:
                print "%s: Pushing [%s>%s] at %s" % (self.name, airportIn.code, airportOut.code, dateIn)
                self.q2.put({
                    'edreams_geoId': airportIn.edreams_geoId
                    ,'edreams_geoOut': airportOut.edreams_geoId
                    ,'dateInFormatted': dateIn
                    ,'dateOutFormatted': None
                    ,'tripType': tripType
                    ,'codeIn': airportIn.code
                    ,'codeOut': airportOut.code
                })