import sys
from optparse import make_option
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger('peace')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

from attacks.models import Attack, Location 

import csv
from dateutil import parser


class Command(BaseCommand):
    """
    From locations in attacks, create separate location objects
    """

    help = " From locations in attacks, create separate location objects"

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
                    action='store_true',
                    default=False,
                    dest='verbose', help='Show more logging info'),

        make_option('--save',
                    action='store_true',
                    default=False,
                    dest='save',
                    help='Whether to actually save the changes to the database.  By default nothing is changed.'),
    )

    def handle(self, *args, **options):

        verbose = options.get('verbose')
        save = options.get('save')

        if verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug('Using verbose output')

        # for each attack:
        # get the location,
        # if not in db, create new location object
        # this is so we can only geocode once, since it's
        # expensive to make calls to google maps
        
        qs = Attack.objects.all()
        total = qs.count()
        count = 0 

        logger.info("Creating locations")
        logger.info("Starting with %s total attacks" % total)

        for a in qs:
            location, created = Location.objects.get_or_create(city=a.city, country=a.country)
            if created:
                print "created location: %s, %s" % (location.city, location.country)
                count +=1

        print "%s locations created, over %s attacks" % (count, total) 