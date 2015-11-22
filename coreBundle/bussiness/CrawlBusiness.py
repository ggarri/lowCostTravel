from coreBundle.crawlers.EdreamsCrawler import EdreamsCrawler
from coreBundle.models.AirportCode import AirportCode
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
            print "Saving Country: %s (%s)" % (country.name, country.code)
            country.save()
        return countries

    def store_aiport_in_country(self, country_code):
        """
        :param country_code: str
        :return: list(Airport)
        """
        country = Country.objects.get(code=country_code)
        airports, airport_codes = self._get_aiports_in_country(country)

        for airport in airports:
            print "Saving Airport: %s - %s at (%s)" % (airport.name, airport.code, country.name)
            airport.save()

        for airport_code in airport_codes:
            print "Saving AirportCode: %s (%s)" % (airport_code.edreams_geoId, airport.code)
            airport_code.save()

        return airports

    @staticmethod
    def reset_airport_is_main_by_country(country_code):
        """
        :param country: str
        :return: None
        """
        country = Country.objects.get(code=country_code)
        Airport.objects.filter(country=country).update(is_main=True)

    # TODO Improve this method
    def get_best_conexion(self, airport_in, country_code):
        out_country = Country.objects.get(code=country_code)
        out_airports = Airport.objects.filter(country=out_country, is_main=True)

        # Calculate global avarage prices
        all_flights = Flight.objects.filter(airport_out__in=out_airports, airport_in=airport_in) \
                      | Flight.objects.filter(airport_in__in=out_airports, airport_out=airport_in)

        all_flight_prices = set(all_flights.values_list('price', flat=True))
        date_range_flights = set(all_flights.values_list('date_in'))

        if 0 == len(all_flight_prices):
            fGlobalAvaragePrice = None
        else:
            fGlobalAvaragePrice = reduce(lambda x, y: x + y, all_flight_prices) / len(all_flight_prices)
            print "Global avarage price %f with %d days crawled" % (fGlobalAvaragePrice, len(date_range_flights))

        # Get the list of airport which has price lower than global avarage
        best_airports = []
        for out_airport in out_airports:
            out_flights = Flight.objects.filter(airport_out=out_airport, airport_in=airport_in) \
                      | Flight.objects.filter(airport_in=out_airport, airport_out=airport_in)

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
                best_airports.append(out_airport)

        return Airport.objects.filter(aiport_in__in=best_airports)

    def store_flights_between_geo_id(self, airport_in_code, airport_out_code, date_from, date_to=None):
        airport_in = Flight.objects.get(code=airport_in_code)
        airport_out = Flight.objects.get(code=airport_out_code)

        stop_over_from = StopOver(airport_in, date=date_from)
        stop_over_to = StopOver(airport_out, date=date_to)

        trip_type = 'ONE_WAY' if date_to is None else 'ROUND_TRIP'

        flights = self._get_flights_between_geo_id(stop_over_from, stop_over_to, trip_type)

        # Deleting old data from the same flights
        Flight.objects.filter(aiport_in=airport_in.geo_id, airport_out=airport_out,
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
                stop_over_from = StopOver(airport_from, date=date_from)
                stop_over_to = StopOver(airport_to, date=date_to)
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

        flights = Flight.objects.filter(airport_in__in=airports_in, airport_out__in=airports_out).exclude(
            price=-1).order_by('price')[:limit]

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
        airport_codes = list()
        for data_airport in data_airports:
            aiport, is_new = Airport.objects.get_or_create(country=country, code=data_airport['code'])
            aiport.city = data_airport['city']
            airports.append(aiport)

            airport_code, is_new = AirportCode.objects.get_or_create(airport=aiport)
            if isinstance(self.crawler, EdreamsCrawler):
                airport_code.edreams_geoId = data_airport['geoId']

            airport_codes.append(aiport)

        return airports, airport_codes

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
            flight = Flight(airport_in=stop_over_from.airport, airport_out=stop_over_to.airport,
                            trip_type=trip_type, date_in=stop_over_from.get_date_formated(),
                            date_out=stop_over_to.get_date_formated(), price=-1)
            flights.append(flight)
        else:
            for data_flight in data_flights:
                flight = Flight(airport_in=stop_over_from.airport, airport_out=stop_over_to.airport,
                                trip_type=trip_type, date_in = stop_over_from.get_date_formated(),
                                date_out=stop_over_to.get_date_formated())

                flight.duration_in = data_flight['durationIn']
                flight.duration_out = data_flight['durationOut']
                flight.stops_in = data_flight['stopsIn']
                flight.stops_out = data_flight['stopsOut']
                flight.price = data_flight['price']
                flights.append(flight)

        return flights