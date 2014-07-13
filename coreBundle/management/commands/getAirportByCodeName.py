from django.core.management.base import BaseCommand, CommandError

import sys
from coreBundle.models import *

class Command(BaseCommand):

    args = '<code_name>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if len(args) < 1:
            print 'EROOR: It must be ' + self.args
            sys.exit(-1)

        code = args[0]
        Airport.storeEdreamsCitiesByCountryCode(code)
