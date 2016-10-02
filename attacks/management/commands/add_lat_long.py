import sys
from optparse import make_option
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger('peace')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

from attacks.models import Attack 

import csv
from dateutil import parser


class Command(BaseCommand):
    """
    get lat and long of attack location and enter into db
    """

    help = "get lat and long of attack location and enter into db"

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


        logger.info("Importing attack data")
        logger.info("Starting with %s total attacks" % total)

        count = 0
        processed = 0

        csvfile = codecs.open('attacks.csv', 'r')
        fieldnames = ['date', 'country', 'city', 'killed', 'injured', 'description']
        csvreader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in csvreader:
            if row['date'] == "date":
                continue
            a = Attack()
            a.date = parser.parse(row['date'])
            a.country = row['country']
            a.city = row['city']
            a.num_dead= row['killed']
            a.num_injured = row['injured'] 
            a.description = row['description'] 
            print a 
            a.save()

            count += 1 

    #         date = models.DateTimeField(blank=True, null=True)
    # city = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    # num_dead = models.IntegerField()
    # num_injured = models.IntegerField()
    # description = models.CharField(max_length=500)


        
        # open csv
        # read record 1-by-1
        # save each one into a model
        # print count at the end
        # do we have some kind of unique identifier? 

        import pdb; pdb.set_trace()

        if save:
            logger.info("%s attacks saved." % count)
        else:
            logger.info("In total: %s attacks will be saved." % count)
