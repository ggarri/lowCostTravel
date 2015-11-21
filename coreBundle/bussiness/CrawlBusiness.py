from coreBundle.models.Flight import Flight

__author__ = 'ggarrido'

from coreBundle.crawlers.CrawlerABC import CrawlerABC
from coreBundle.models.Country import Country
from coreBundle.models.Airport import Airport
from coreBundle.models.StopOver import StopOver
import time


class CrawlBusiness():
    """
    :type crawler: CrawlerABC
    """
    crawler = None
    
    def __init__(self, crawler):
        """
        :param crawler: CrawlerABC
        """
        self.crawler = crawler

    def store_countries_start_with(self, letter):
        """
        :param letter: str
        :return: list(Country)
        """
        countries = self._get_countries_start_with(letter)
        for country in countries:
            country.save()
        return countries

    def save_country_code(self):
        for letter in list(map(chr, range(97, 123))):
            self.store_country_code_by_letter(letter)

    def store_aiport_in_country(self, country_code):
        """
        :param country_code: str
        :return: list(Airport)
        """
        country = Country.objects.get(code=country_code)
        airports = self._get_aiports_in_country(country)
        for airport in airports:
            airport.save()
        return airports

    @staticmethod
    def reset_airport_is_main_by_country(country_code):
        """
        :param country: str
        :return: None
        """
        country = Country.objects.get(code=country_code)
        Airport.objects.filter(country=country).update(is_main=True)

    def get_best_conexion(self, country_code):
        out_country = Country.objects.get(code=country_code)
        out_airports = Airport.objects.filter(country=out_country, is_main=True)

        # Calculate global avarage prices
        all_flights = Flight.objects.filter(edreams_geoId_in=self.edreams_geoId
                                       , edreams_geoId_out__in=out_airports.values_list('edreams_geoId')) \
                      | Flight.objects.filter(edreams_geoId_out=self.edreams_geoId
                                       , edreams_geoId_in__in=out_airports.values_list('edreams_geoId'))

        all_flight_prices = set(all_flights.values_list('price', flat=True))
        date_range_flights = set(all_flights.values_list('date_in'))

        if 0 == len(all_flight_prices):
            fGlobalAvaragePrice = None
        else:
            fGlobalAvaragePrice = reduce(lambda x, y: x + y, all_flight_prices) / len(all_flight_prices)
            print "Global avarage price %f with %d days crawled" % (fGlobalAvaragePrice, len(date_range_flights))

        # Get the list of airport which has price lower than global avarage
        best_geo_id_airports = []
        for out_airport in out_airports:
            out_flights = Flight.objects.filter(edreams_geoId_in=self.edreams_geoId
                                       , edreams_geoId_out=out_airport.edreams_geoId) \
                      | Flight.objects.filter(edreams_geoId_out=self.edreams_geoId
                                       , edreams_geoId_in=out_airport.edreams_geoId)

            out_flight_prices = set(out_flights.values_list('price', flat=True))

            # It wasn't crawled it, then give it a chance ;)
            if 0 != len(out_flight_prices):
                fPriceAirportAvarage = reduce(lambda x, y: x + y, out_flight_prices) / len(out_flight_prices)
                # print "Airport %s avarage price %f" % (oAirporOut.city, fPriceAirportAvarage)
            else:
                fPriceAirportAvarage = -1

            # If there is not previous experience, or avarage price is lower or there isn't more than 1 day crawled
            # print fPriceAirportAvarage < fGlobalAvaragePrice, fPriceAirportAvarage, fGlobalAvaragePrice
            if None == fGlobalAvaragePrice or (fPriceAirportAvarage < fGlobalAvaragePrice and fPriceAirportAvarage > 0) \
                    or len(date_range_flights) < 3:
                best_geo_id_airports.append(out_airport.edreams_geoId)

        return Airport.objects.filter(edreams_geoId__in=best_geo_id_airports)

    def store_flights_between_geo_id(self, geo_id_from, geo_id_to, date_from, date_to=None):
        stop_over_from = StopOver(geo_id=geo_id_from, date=date_from)
        stop_over_to = StopOver(geo_id=geo_id_to, date=date_to)
        trip_type = 'ONE_WAY' if date_to is None else 'ROUND_TRIP'

        flights = self._get_flights_between_geo_id(stop_over_from, stop_over_to, trip_type)

        # Deleting old data from the same flights
        Flight.objects.filter(edreams_geoId_in=stop_over_from.geo_id, edreams_geoId_out=stop_over_to.geo_id,
                              trip_type=trip_type, date_in=stop_over_from.get_date_formated,
                              date_out=stop_over_to.get_date_formated).delete()

        for flight in flights:
            flight.save()
        return flights

    def store_flight_between_countries(self, country_code_from, country_code_to, date_from, date_to=None,
                                       only_main=True):
        trip_type = 'ONE_WAY' if date_to is None else 'ROUND_TRIP'
        country_from = Country.objects.get(code=country_code_from)
        country_to = Country.objects.get(code=country_code_to)
        airports_from = Airport.objects.filter(country=country_from, is_main=only_main)
        """:type : Airport """
        airports_to = Airport.objects.filter(country=country_to, is_main=only_main)
        """:type : Airport """

        flights = list()
        for airport_from in airports_from:
            for airport_to in airports_to:
                stop_over_from = StopOver(geo_id=airport_from.geo_id, date=date_from)
                stop_over_to = StopOver(geo_id=airport_to.geo_id, date=date_to)
                _flights = self._get_flights_between_geo_id(stop_over_from, stop_over_to, trip_type)
                flights.append(_flights)

        for flight in flights:
            flight.save()
        return flights

    def get_list_cheapest_flight(self, code_in, code_out, limit=10):
        """
        :param code_in: string
        :param code_out: string
        :param limit: int
        :return: list(Flight)
        """
        if len(code_in) == 2:
            country_in = Country.objects.get(code=code_in)
            airports_in = Airport.objects.filter(country=country_in)
        else:
            airports_in = Airport.objects.filter(code=code_in)

        if len(code_out) == 2:
            country_out = Country.objects.get(code=code_out)
            airports_out = Airport.objects.filter(country=country_out)
        else:
            airports_out = Airport.objects.filter(code=code_out)

        flights = Flight.objects.filter(edreams_geoId_in__in=airports_in.values_list('edreams_geoId', flat=True),
                              edreams_geoId_out__in=airports_out.values_list('edreams_geoId', flat=True)
                              ).exclude(price=-1).order_by('price')[:limit]
        return flights

    ############################################
    #   PROTECTED METHODS
    ############################################

    def _get_countries_start_with(self, letter):
        """
        :param letter: str
        :return: list(Country)
        """
        code_names = self.crawler.get_countries(letter)
        countries = list()

        for code_name in code_names:
            country, is_new = Country.objects.get_or_create(code=code_name['code'])
            country.name = code_name['name']
            countries.append(country)
        return countries

    def _get_aiports_in_country(self, country):
        """
        :param country: Country
        :return: list(Airport)
        """
        data_airports = self.crawler.get_aiports(country.code)
        airports = list()
        for data_airport in data_airports:
            aiport, is_new = Airport.objects.get_or_create(edreams_geoId=data_airport['geoId'], country=country,
                                                                code=data_airport['code'])
            aiport.city = data_airport['city']
            airports.append(aiport)
        return airports

    def _get_flights_between_geo_id(self, stop_over_from, stop_over_to, trip_type='ONE_WAY'):
        """
        :param trip_type: str
        :param stop_over_from: StopOver
        :param stop_over_to: StopOver
        :return: list(Flight)
        """

        data_flights = self.crawler.get_flights(trip_type, stop_over_from, stop_over_to)
        flights = list()
        if len(data_flights) == 0:
            flight = Flight(edreams_geoId_in=stop_over_from.geo_id, edreams_geoId_out=stop_over_to.geo_id,
                            trip_type=trip_type, date_in=stop_over_from.get_date_formated(),
                            date_out=stop_over_to.get_date_formated(), price=-1)
            flights.append(flight)
        else:
            for data_flight in data_flights:
                flight = Flight(edreams_geoId_in=stop_over_from.geo_id, edreams_geoId_out=stop_over_to.geo_id,
                                   trip_type=trip_type, date_in = stop_over_from.get_date_formated(),
                                   date_out=stop_over_to.get_date_formated())

                flight.duration_in = data_flight['durationIn']
                flight.duration_out = data_flight['durationOut']
                flight.stops_in = data_flight['stopsIn']
                flight.stops_out = data_flight['stopsOut']
                flight.price = data_flight['price']
                flights.append(flight)

        return flights