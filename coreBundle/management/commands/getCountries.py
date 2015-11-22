from django.core.management.base import BaseCommand, CommandError

import sys
from string import ascii_lowercase
from coreBundle.bussiness.CrawlBusiness import CrawlBusiness
from coreBundle.crawlers.EdreamsCrawler import EdreamsCrawler


class Command(BaseCommand):

    args = '<letter>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        crawler = EdreamsCrawler()
        bussiness = CrawlBusiness(crawler)

        if len(args) < 1:
            for letter in ascii_lowercase:
                bussiness.store_countries_start_with(letter)
        else:
            letter = args[0]
            bussiness.store_countries_start_with(letter)
