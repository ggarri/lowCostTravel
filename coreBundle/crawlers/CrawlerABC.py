__author__ = 'ggarrido'

from abc import ABCMeta, abstractmethod
import urllib
import urllib2
from bs4 import BeautifulSoup
import pycurl
import StringIO


class CrawlerABC():
    __metaclass__ = ABCMeta

    proxy_ip = None
    proxy_port = None

    headers = {
        'Pragma': 'no-cache'
        , 'Origin': 'http://www.edreams.es'
        , 'Host': 'www.edreams.es'
        , 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 '
                        'Safari/537.36'
        , 'Content-Type': 'application/x-www-form-urlencoded'
        , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        , 'Cache-Control': 'no-cache, must-revalidate'
        , 'Referer': 'http://www.edreams.es/engine/ItinerarySearch/search'
        , 'Connection': 'keep-alive'
    }

    def __init__(self, ip='127.0.0.1', port=9050):
        self.proxy_ip = ip
        self.proxy_port = port

    @abstractmethod
    def get_flights(self, trip_type, dep_stop, arr_stop):
        pass

    @abstractmethod
    def get_aiports(self, country_code):
        pass

    @abstractmethod
    def get_countries(self, letter):
        pass

    @abstractmethod
    def _extract_fligh_data_oneway(self, html):
        pass

    @abstractmethod
    def _extract_fligh_data_roundtrip(self, html):
        pass

    def get_html(self, url, params):
        data = urllib.urlencode(params)
        req = urllib2.Request(url)
        for headType, headValue in self.headers.items():
            req.add_header(headType, headValue)

        response = urllib2.urlopen(req, data)
        html = response.read()
        return html

    def get_html_proxy(self, url, params):
        output = StringIO.StringIO()
        params = urllib.urlencode(params)

        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.POSTFIELDS, params)
        headers = [(x+': '+y) for x, y in self.headers.iteritems() ]

        c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.PROXY, self.proxy_ip)
        c.setopt(pycurl.PROXYPORT, self.proxy_port)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        c.setopt(pycurl.WRITEFUNCTION, output.write)

        try:
            c.perform()
            return output.getvalue()
        except pycurl.error as exc:
            return "Unable to reach %s (%s)" % (url, exc)

    @staticmethod
    def covert_html2beauti_soup(html):
        soup = BeautifulSoup(html)
        return soup

    @staticmethod
    def file_write(file_name, text):
        f = open(file_name, 'w')
        f.write(text)
        f.close()

