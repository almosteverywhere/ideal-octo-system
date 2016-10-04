import sys
from optparse import make_option
from django.core.management.base import BaseCommand
import logging
import googlemaps

logger = logging.getLogger('peace')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

from attacks.models import Attack, Location 

import csv
from dateutil import parser
# AIzaSyDv47jLb3cJ9H-ttYVKPAyPGoa2Yl3zd-A
# gmaps = googlemaps.Client(key='AIzaSyAApYWyjVYCXs3P91Fn7NEu85XUu9Jpvm0')
gmaps = googlemaps.Client(key='AIzaSyCYZUr3mfLai-9WsnAkd3cW40zWsQuXl2c')

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

        for l in qs:

            # don't re-geocode 
            # if both are 0, haven't done before, if both are -1, can't find it, don't retry   
            if (l.lat == 0 and l.lng == 0):
                location_string = "%s, %s" % (l.city, l.country)
                
                geocode_result = gmaps.geocode(location_string)
                    # print "result for %s %s" % (location, geocode_result)
                if geocode_result:
                    count += 1 
                    try:
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']
                    except:
                        import pdb; pdb.set_trace()
                        l.lat = -1
                        l.lng = -1
                        l.save()
                
                    
                    l.lat = lat
                    l.lng = lng
                    l.save()
                    print "Saving lat and long for %s: lat %s, lng %s" % (location_string, lat, lng)

                if not geocode_result:
                    print "No result for location %s" % location_string
                    not_found +=1
                    l.lat = -1
                    l.lng = -1
                    l.save()

            
        if save:
            logger.info("%s attacks saved." % count)
            logger.info("%s result not found." % not_found)
        else:
            logger.info("In total: %s attacks will be saved." % count)
            logger.info("%s result not found." % not_found)
