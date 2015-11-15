__author__ = 'ggarrido'

from coreBundle.crawlers.CrawlerABC import CrawlerABC
from html import *
import re


class EdreamsCrawler(CrawlerABC):
    def get_flights(self, trip_type, dep_stop, arr_stop):
        """
        :param trip_type: string
        :param dep_stop: StopOver
        :param arr_stop: StopOver
        :return: list
        """

        url = 'http://www.edreams.es/engine/ItinerarySearch/search'
        params = {
            'departureLocationGeoNodeId': dep_stop.geo_id
            , 'departureLocation': dep_stop.city
            , 'departureDate': dep_stop.date
            , 'departureTime': '0000'
            , 'arrivalLocationGeoNodeId': arr_stop.geo_id
            , 'arrivalLocation': arr_stop.city
            , 'returnDate': arr_stop.date
            , 'returnTime': '0000'
            , 'country': 'ES'
            , 'language': 'es'
            , 'numAdults': 1
            , 'numChilds': 0
            , 'numInfants': 0
            , 'searchMainProductTypeName': 'FLIGHT'
            , 'tripTypeName': trip_type
            , 'applyAllTaxes': 'true'
            , 'resultsFromSearch': 'true'
        }

        if self.proxy_port and self.proxy_ip:
            html = self.get_html_proxy(url, params)
        else:
            html = self.get_html(url, params)

        self.write_file("last_crawled.html", html)

        if trip_type == 'ROUND_TRIP':
            return self._extract_fligh_data_roundtrip(self, html)
        elif trip_type == 'ONE_WAY':
            return self._extract_fligh_data_oneway(self, html)

        return list()

    def get_aiports(self, country_code):
        url = 'http://www.edreams.es/engine/searchEngines/pickers/locationsPerCountry.jsp'
        params = {'countryCode': country_code }
        html = self.get_html(url, params)
        soup = self.covert_html2beauti_soup(html)
        city_aiports = list()
        list_code = soup.find(id='countryDestinationsCodesArray').string.split('|')
        list_geo_id = soup.find(id='countryDestinationsGeoNodeIdsArray').string.split('|')
        list_geo_id_by_code = dict(zip(list_code, list_geo_id))

        for span in soup.find_all('span', class_='paddedCities'):
            city = span.a.get('title').strip()
            code = span.a.get('id').strip().replace('countryDestination_', '')
            geo_Id = list_geo_id_by_code[code]
            city_aiport = {'city': city, 'geoId': geo_Id, 'code': code}
            city_aiports.append(city_aiport)

        return city_aiports

    def get_countries(self, letter):
        url = 'http://www.edreams.es/engine/searchEngines/pickers/countriesPerLetter.jsp'
        params = {'letter': letter}
        html = self.get_html(url, params)
        soup = self.covert_html2beauti_soup(html)
        country_codes = list()

        for td in soup.find_all('td'):
            country_and_code = td.a.get('id')
            if 'country' in country_and_code:
                code_name = {'code': country_and_code.replace('country', ''), 'name': td.a.string.strip()}
                country_codes.append(code_name)

        return country_codes

    def _extract_fligh_data_oneway(self, html):
        soup = self.covert_html2beauti_soup(html)
        flight_list = list()
        for idx, div in enumerate(soup.find_all('div', class_='singleItineray-content')):
            info = {'durationIn': None, 'stopsIn': None, 'price': None, 'durationOut': None, 'stopsOut': None}
            try:
                # Price
                price_div = div.find(class_='singleItinerayPrice')
                price_string = (price_div.contents[2].replace('.',''))+(price_div.find(class_='decimalPricePart').string.replace(',','.'))
                price = float(price_string)
                info['price'] = price

                # Duration
                duration_out = div.find(id='segmentElapsedTime_%d_out0' % idx).string
                regexp = "(\d+)h(\d+)"
                duration_out_items = re.findall(regexp, duration_out)
                duration_in_string = "%sh%sm" % (duration_out_items[0])
                info['duration_out'] = duration_in_string

                # Stops
                stop_out = div.find(id='segmentStopsOvers_%d_out0' % idx).string
                regexp = "(\d+)"
                stop_out_items = re.findall(regexp, stop_out)
                stop_out_string = int(stop_out_items[0])
                info['stopsOut'] = stop_out_string
                flight_list.append(info)

            except:
                flight_list.append(info)

        return flight_list

    def _extract_fligh_data_roundtrip(self, html):
        soup = self.covert_html2beauti_soup(html)
        flight_list = list()

        for idx, div in enumerate(soup.find_all('div', class_='singleItineray-content')):
            info = {'price': None,
                    'durationIn': None,
                    'durationOut': None,
                    'stopsIn': None,
                    'stopsOut': None
            }

            try:
                # Price
                price_div = div.find(class_='singleItinerayPrice')
                price_string = (price_div.contents[2].replace('.', '')) + (price_div.find(class_='decimalPricePart').string.replace(',', '.'))
                price = float(price_string.replace(',', '.'))
                info['price'] = price

                # Duration
                duration_in = div.find(id='segmentElapsedTime_%d_in0' % idx).string
                duration_out = div.find(id='segmentElapsedTime_%d_out0' % idx).string
                regexp = "(\d+)h(\d+)"
                duration_in_items = re.findall(regexp, duration_in)
                duration_out_items = re.findall(regexp, duration_out)
                duration_in_string = "%sh%sm" % (duration_in_items[0])
                duration_out_string = "%sh%sm" % (duration_out_items[0])
                info['durationIn'] = duration_in_string
                info['duration_out'] = duration_out_string
                # Stops
                stop_in = div.find(id='segmentStopsOvers_%d_in0' % idx).string
                stop_out = div.find(id='segmentStopsOvers_%d_out0' % idx).string
                regexp = "(\d+)"
                stop_in_items = re.findall(regexp, stop_in)
                stop_out_items = re.findall(regexp, stop_out)
                stop_in_string = int(stop_in_items[0])
                stop_out_string = int(stop_out_items[0])
                info['stopsIn'] = stop_in_string
                info['stopsOut'] = stop_out_string
                flight_list.append(info)

            except:
                flight_list.append(info)

        return flight_list

