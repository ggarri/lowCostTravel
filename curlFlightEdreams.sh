#!/bin/sh
curl 'http://www.edreams.es/engine/ItinerarySearch/search' \
-H 'Pragma: no-cache' \
-H 'Origin: http://www.edreams.es' \
-H 'Accept-Encoding: gzip,deflate,sdch' \
-H 'Accept-Language: en-GB,en;q=0.8,es;q=0.6,en-US;q=0.4' \
-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
-H 'Cache-Control: no-cache'
-H 'Referer: http://www.edreams.es/' \
-H 'Connection: keep-alive' \
--data 'buyPath=1&
auxOrBt=0&
searchMainProductTypeName=FLIGHT&
departureLocationGeoNodeId=&
arrivalLocationGeoNodeId=&
tripTypeName=ROUND_TRIP&
departureLocation=Madrid&
departureDate=19%2F08%2F2014&
departureTime=0000&
numAdults=1&
numChilds=0&
numInfants=0&
cabinClassName=&
filteringCarrier=&
fake_filteringCarrier=Todas+las+compa%C3%B1%C3%ADas&
collectionTypeEstimationNeeded=false&
applyAllTaxes=false&
resultsFromSearch=true&
arrivalLocation=Barcelona&
returnDate=26%2F08%2F2014&
returnTime=0000&
country=ES&
language=es&
numberOfRooms=1&room0Adults=1&room1Adults=1&room2Adults=1&room3Adults=1&room0Childs=0&room0Child0Age=0&room0Child1Age=0&room1Childs=0&room1Child0Age=0&room1Child1Age=0&room2Childs=0&room2Child0Age=0&room2Child1Age=0&room3Childs=0&room3Child0Age=0&room3Child1Age=0' \
--compressed

tripTypeName=ROUND_TRIP&arrivalLocationGeoNodeId=&departureDate=19%2F10%2F2014&resultsFromSearch=true&numAdults=1&fake_filteringCarrier=Todas+las+compa%C3%B1%C3%ADas&auxOrBt=0&departureLocation=Madrid&applyAllTaxes=false&collectionTypeEstimationNeeded=false&numInfants=0&arrivalLocation=Barcelona&searchMainProductTypeName=FLIGHT&numChilds=0&departureTime=0000&language=es&arrivalDate=20%2F10%2F2014&country=ES&cabinClassName=&departureLocationGeoNodeId=&buyPath=3&returnTime=0000