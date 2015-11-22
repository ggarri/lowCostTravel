__author__ = 'ggarrido'

import time


class StopOver():
    geo_id = None
    city = None
    date = None
    country = None

    def __init__(self, airport, city, date, country):
        self.airport = airport
        self.city = city
        self.date = date
        self.country = country

    def get_date_formated(self):
        if self.date is None:
            return None
        date_in_tmp = time.strptime(self.date, "%d/%m/%Y")
        return time.strftime("%Y-%m-%d", date_in_tmp)
