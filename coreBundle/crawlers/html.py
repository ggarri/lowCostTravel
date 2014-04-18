import urllib
import urllib2
from bs4 import BeautifulSoup

def getHtml(url, params):
	params = urllib.urlencode(params)
	response = urllib2.urlopen(url, params)
	html = response.read()
	return html

def getHtml2(url, params):
    data = urllib.urlencode(params)
    req = urllib2.Request(url)
    req.add_header('Pragma', 'no-cache')
    req.add_header('Origin', 'http://www.edreams.es')
    # req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
    # req.add_header('Accept-Language', 'en-GB,en;q=0.8,es;q=0.6,en-US;q=0.4')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Referer', 'http://www.edreams.es/')
    req.add_header('Connection', 'keep-alive')
    response = urllib2.urlopen(req, data)
    html = response.read()
    return html


def covertHtml2BeautiSoup(html):
	soup = BeautifulSoup(html)
	return soup
