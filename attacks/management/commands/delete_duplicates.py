import sys
from optparse import make_option
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger('peace')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

from attacks.models import Attack 

import csv
import codecs
from dateutil import parser

class Command(BaseCommand):
    """
    delete duplicate attacks, have no idea how they got there
    """
    help = "delete duplicate attacks"

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

        qs = Attack.objects.all()
        total = qs.count()

        
        logger.info("Deleting duplicate attacks")
        logger.info("Starting with %s total attacks" % total)

        count = 0
        processed = 0
        dupes = 0   
        dupe_count = 1

        # kind of lazy way to do this
        for a in Attack.objects.all():
            dupes = Attack.objects.all().filter(description=a.description).filter(date=a.date).filter(num_dead=a.num_dead).filter(city=a.city)
            if dupes.count() > 1:
                dupe_count = 1
                # delete all but first one
                # could use queryset delete but this is simpler 
                for d in dupes[1:]:
                    print "DUP #%s" % dupe_count
                    print "num of dupes total %s" % dupes.count() 
                    print "deleting dupes for %s" % d.description
                    # print d.num_dead
                    # print d.city
                    dupe_count += 1
                    if save:
                        d.delete()
                print "deleted %s dupes for %s" % (dupe_count, a.description) 

                print "*" * 10

        # if save:
        #     logger.info("%s attacks saved." % count)
        # else:
        #     logger.info("In total: %s attacks will be saved." % count)
