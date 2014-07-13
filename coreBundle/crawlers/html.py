import urllib
import urllib2
from bs4 import BeautifulSoup
import pycurl
import StringIO

eDreamsHeaders = {
    'Pragma': 'no-cache'
    , 'Origin': 'http://www.edreams.es'
    , 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'
    , 'Content-Type': 'application/x-www-form-urlencoded'
    , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    , 'Cache-Control': 'no-cache'
    , 'Referer': 'http://www.edreams.es/'
    , 'Connection': 'keep-alive'
}

def getHtml(url, params):
	params = urllib.urlencode(params)
	response = urllib2.urlopen(url, params)
	html = response.read()
	return html

def getHtml2(url, params):
    data = urllib.urlencode(params)
    req = urllib2.Request(url)
    for headType, headValue in eDreamsHeaders.items() :
        print headType, headValue
        req.add_header(headType, headValue)

    response = urllib2.urlopen(req, data)
    html = response.read()
    return html

    # req.add_header('Pragma', 'no-cache')
    # req.add_header('Origin', 'http://www.edreams.es')
    # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36')
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    # req.add_header('Cache-Control', 'no-cache')
    # req.add_header('Referer', 'http://www.edreams.es/')
    # req.add_header('Connection', 'keep-alive')

def getHtmlProxy(url, params, ip = None, port = None):
    output = StringIO.StringIO()
    params = urllib.urlencode(params)

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POSTFIELDS, params)
    headers = [ (x+': '+y) for x,y in eDreamsHeaders.iteritems() ]

    c.setopt(pycurl.HTTPHEADER, headers)

    if port != None and ip != None:
        c.setopt(pycurl.PROXY, ip)
        c.setopt(pycurl.PROXYPORT, port)
        c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)

    c.setopt(pycurl.WRITEFUNCTION, output.write)

    try:
        c.perform()
        return output.getvalue()
    except pycurl.error as exc:
        return "Unable to reach %s (%s)" % (url, exc)


def covertHtml2BeautiSoup(html):
	soup = BeautifulSoup(html)
	return soup


def fileWrite(fileName, text):
    f = open(fileName, 'w')
    f.write(text)
    f.close()

