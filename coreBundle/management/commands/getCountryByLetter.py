from django.core.management.base import BaseCommand, CommandError

import sys
from coreBundle.bussiness.CrawlBusiness import CrawlBussiness
from coreBundle.crawlers import EdreamsCrawler
from coreBundle.models import *

class Command(BaseCommand):

    args = '<letter>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if len(args) < 1:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)
        else:
            letter = args[0]

        crawler = EdreamsCrawler()
        bussiness = CrawlBussiness(crawler)
        bussiness.store_countries_start_with(letter)
