lowCostTravel
=============

Run services
----------------

* Mysql services running 
$ systemctl start mysqld

* tor service running
This is not totally necesary to use it, but in case you want to use proxies, it is a must. 
$ systemctl start tor


Starting the project
-------------------

* Initialize the database structure
$ python manage.py syncdb

* Populating database with initial data.
** Obtaining country available letter by letter from "source" web. 
$ python manage.py getCountryByLetter [A-Z]

** Filling up database with every airport locate into an specify country
$ python manage.py getAirportByCodeName [ES|UK|US|FR]

** Crawling fligh prices between AirportCode|CountryCode <> AirportCode|CountryCode, within date range
$ python manage.py getFlights [ES|MAD] [US|JFK] from_d/m/Y dest_d/m/Y


Version
----------
Current version 0.0.8


License
---------

GNU GENERAL PUBLIC LICENSE






