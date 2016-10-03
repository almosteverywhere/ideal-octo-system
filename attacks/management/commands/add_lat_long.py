import sys
from optparse import make_option
from django.core.management.base import BaseCommand
import logging
import googlemaps

logger = logging.getLogger('peace')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

from attacks.models import Attack 

import csv
from dateutil import parser

gmaps = googlemaps.Client(key='AIzaSyAApYWyjVYCXs3P91Fn7NEu85XUu9Jpvm0')

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

        # for each attack:
        # get the location,
        # send to google maps
        # get the lat and long coordinates
        # maybe use memoization so don't have to repeat
        # the same query a million times? 
        # info is denormalized in the db because don't
        # want to deal with different locations 
        # dealing with locations is the worsssssse

        qs = Location.objects.all()
        total = qs.count()
        count = 0 
        not_found = 0

        logger.info("Adding lat long to locations")
        logger.info("Starting with %s total locations" % total)

        locations = {}
        import pdb; pdb.set_trace()
        for a in qs:
            if not a.lat and not a.long:
                location = "%s, %s" % (a.city, a.country)
                # use memoization
                if location in locations:
                    pass 
                    # locations[location] += 1
                else:
                    geocode_result = gmaps.geocode(location)
                    # print "result for %s %s" % (location, geocode_result)
                    if geocode_result:
                        count += 1 
                        try:
                            lat = geocode_result[0]['geometry']['location']['lat']
                            lng = geocode_result[0]['geometry']['location']['lng']
                        except:
                            import pdb; pdb.set_trace()
                    
                        locations[location] = {}
                        locations[location]['lat'] = lat
                        locations[location]['lng'] = lng
                        if save:
                            a.latitude = lat
                            a.longitude = lng
                            a.save()
                    if not geocode_result:
                        print "No result for location %s" % location
                        not_found +=1

            for k in locations.keys():
                print "%s: %s" % (k, locations[k])

        # write it to a csv:


        # count = 0
        # processed = 0

        # csvfile = codecs.open('attacks.csv', 'r')
        # fieldnames = ['date', 'country', 'city', 'killed', 'injured', 'description']
        # csvreader = csv.DictReader(csvfile, fieldnames=fieldnames)

        # for row in csvreader:
        #     if row['date'] == "date":
        #         continue
        #     a = Attack()
        #     a.date = parser.parse(row['date'])
        #     a.country = row['country']
        #     a.city = row['city']
        #     a.num_dead= row['killed']
        #     a.num_injured = row['injured'] 
        #     a.description = row['description'] 
        #     print a 
        #     a.save()

        #     count += 1 

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

        if save:
            logger.info("%s attacks saved." % count)
            logger.info("%s result not found." % not_found)
        else:
            logger.info("In total: %s attacks will be saved." % count)
            logger.info("%s result not found." % not_found)
