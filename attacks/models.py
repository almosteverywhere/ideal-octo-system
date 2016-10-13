from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Attack(models.Model):
    date = models.DateField(blank=True, null=True)
    
    num_dead = models.IntegerField()
    num_injured = models.IntegerField()
    description = models.CharField(max_length=500)

    # soon to delete these fields once we've migrated the locations
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    # let it be null for now while we populate relationship
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    

    class Meta:
        unique_together = ('date', 'description')

    def __unicode__(self):
        return '%s, %s: %s' % (self.city, self.country, self.description)

    # class Meta:
    # unique_together = ('field1', 'field2',)

class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    class Meta:
        unique_together = ('city', 'country')

    def __unicode__(self):
        return '%s, %s' % (self.city, self.country)

