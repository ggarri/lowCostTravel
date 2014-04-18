import urllib
import urllib2
from bs4 import BeautifulSoup

def getHtml(url, params):
	params = urllib.urlencode(params)
	response = urllib2.urlopen(url, params)
	html = response.read()
	return html

def covertHtml2BeautiSoup(html):
	soup = BeautifulSoup(html)
	return soup
