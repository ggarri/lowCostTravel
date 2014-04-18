from html import *

def getEdreamCrawledAiports(countryCode = 'DE'):

    url = 'http://www.edreams.es/engine/searchEngines/pickers/locationsPerCountry.jsp'
    params = {'countryCode': countryCode }
    html = getHtml(url, params)
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