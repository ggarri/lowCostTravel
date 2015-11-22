from django.core.management.base import BaseCommand, CommandError

import sys
from coreBundle.bussiness.CrawlBusiness import CrawlBusiness
from coreBundle.crawlers.EdreamsCrawler import EdreamsCrawler


class Command(BaseCommand):

    args = '<code_name>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if len(args) < 1:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)
        else:
            code = args[0]

        crawler = EdreamsCrawler()
        bussiness = CrawlBusiness(crawler)
        bussiness.store_aiport_in_country(code)
