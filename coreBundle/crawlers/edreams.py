# -*- coding: utf-8 -*-
from html import *
import re

proxy_ip = '127.0.0.1'
proxy_port = 9050
proxy_active = True

def _extractFlighDataOneWay(html):
    soup = covertHtml2BeautiSoup(html)
    flightList = list()
    for idx, div in enumerate(soup.find_all('div', class_='singleItineray-content')):
        info = {'durationIn': None, 'stopsIn': None, 'price': None, 'durationOut': None, 'stopsOut': None}
        try:
            #Price
            priceDiv = div.find(class_='singleItinerayPrice')
            priceString = (priceDiv.contents[2].replace('.',''))+(priceDiv.find(class_='decimalPricePart').string.replace(',','.'))
            price = float(priceString)
            info['price'] = price

            # Duration
            durationOut = div.find(id='segmentElapsedTime_%d_out0' % (idx)).string
            regexp = "(\d+)h(\d+)"
            durationOutItems = re.findall(regexp, durationOut)
            durationOutString = "%sh%sm" % (durationOutItems[0])
            info['durationOut'] = durationOutString

            # Stops
            stopOut = div.find(id='segmentStopsOvers_%d_out0' % (idx)).string
            regexp = "(\d+)"
            stopOutItems = re.findall(regexp, stopOut)
            stopOutString = int(stopOutItems[0])
            info['stopsOut'] = stopOutString

            flightList.append(info)
        except:
            flightList.append(info)


    return flightList


def _extractFlighDataRoundTrip(html):
    soup = covertHtml2BeautiSoup(html)
    flightList = list()

    for idx, div in enumerate(soup.find_all('div', class_='singleItineray-content')):
        info = {
          'price': None
           , 'durationIn': None
           , 'durationOut': None
           , 'stopsIn': None
           , 'stopsOut': None
        }
        try:
            #Price
            priceDiv = div.find(class_='singleItinerayPrice')
            priceString = (priceDiv.contents[2].replace('.',''))+(priceDiv.find(class_='decimalPricePart').string.replace(',','.'))
            price = float(priceString.replace(',','.'))
            info['price'] = price
            # Duration
            durationIn = div.find(id='segmentElapsedTime_%d_in0' % (idx)).string
            durationOut = div.find(id='segmentElapsedTime_%d_out0' % (idx)).string
            regexp = "(\d+)h(\d+)"
            durationInItems = re.findall(regexp, durationIn)
            durationOutItems = re.findall(regexp, durationOut)
            durationInString = "%sh%sm" % (durationInItems[0])
            durationOutString = "%sh%sm" % (durationOutItems[0])
            info['durationIn'] = durationInString
            info['durationOut'] = durationOutString
            # Stops
            stopIn = div.find(id='segmentStopsOvers_%d_in0' % (idx)).string
            stopOut = div.find(id='segmentStopsOvers_%d_out0' % (idx)).string
            regexp = "(\d+)"
            stopInItems = re.findall(regexp, stopIn)
            stopOutItems = re.findall(regexp, stopOut)
            stopInString = int(stopInItems[0])
            stopOutString = int(stopOutItems[0])
            info['stopsIn'] = stopInString
            info['stopsOut'] = stopOutString

            flightList.append(info)
        except:
            flightList.append(info)

    return flightList

def getEdreamCrawledFlights(tripType, departureGeoId, arrivalGeoId, departureCity, arrivalCity, departureDate, arrivalDate):
    url = 'http://www.edreams.es/engine/ItinerarySearch/search'
    params = {
        'departureLocationGeoNodeId': departureGeoId
        , 'departureLocation': departureCity
        , 'departureDate': departureDate
        , 'departureTime': '0000'
        , 'arrivalLocationGeoNodeId': arrivalGeoId
        , 'arrivalLocation': arrivalCity
        , 'returnDate': arrivalDate
        , 'returnTime': '0000'
        , 'country': 'ES'
        , 'language': 'es'
        , 'numAdults': 1
        , 'numChilds': 0
        , 'numInfants': 0
        , 'searchMainProductTypeName': 'FLIGHT'
        , 'tripTypeName': tripType
        # , 'numberOfRooms': 1
        # , 'buyPath': 1
        # , 'auxOrBt': 0
        # , 'applyAllTaxes': 'false'
        # , 'cabinClassName': ''
        # , 'filteringCarrier': ''
        # , 'fake_filteringCarrier': "Todas las compañías"
        # , 'collectionTypeEstimationNeeded': 'false'
        # , 'resultsFromSearch': 'true'
    }

    if proxy_active == True:
        html = getHtmlProxy(url, params, proxy_ip, proxy_port)
    else:
        html = getHtml2(url, params)

    if tripType == 'ROUND_TRIP':
        return _extractFlighDataRoundTrip(html)
    elif tripType == 'ONE_WAY':
        return _extractFlighDataOneWay(html)

    return list()



def getEdreamCrawledAiports(countryCode):

    url = 'http://www.edreams.es/engine/searchEngines/pickers/locationsPerCountry.jsp'
    params = {'countryCode': countryCode }
    html = getHtml2(url, params)
    soup = covertHtml2BeautiSoup(html)
    cityAiports = list()
    listCode = soup.find(id='countryDestinationsCodesArray').string.split('|')
    listGeoId = soup.find(id='countryDestinationsGeoNodeIdsArray').string.split('|')
    listGeoIdByCode = dict(zip(listCode, listGeoId))

    for span in soup.find_all('span', class_='paddedCities'):
        city = span.a.get('title').strip()
        code = span.a.get('id').strip().replace('countryDestination_', '')
        geoId = listGeoIdByCode[code]
        cityAiport = {'city': city, 'geoId': geoId, 'code': code}
        cityAiports.append(cityAiport)

    return cityAiports

def getEdreamCrawledCountries(letter):

    url = 'http://www.edreams.es/engine/searchEngines/pickers/countriesPerLetter.jsp'
    params = {'letter': letter}
    html = getHtml(url, params)
    soup = covertHtml2BeautiSoup(html)
    countryCodes = list()

    for td in soup.find_all('td'):
        countryAndCode = td.a.get('id')
        if 'country' in countryAndCode:
            codeName = {'code': countryAndCode.replace('country', ''), 'name': td.a.string.strip()}
            countryCodes.append(codeName)

    return countryCodes


