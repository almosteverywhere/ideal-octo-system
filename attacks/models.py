from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Attack(models.Model):
    date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    num_dead = models.IntegerField()
    num_injured = models.IntegerField()
    description = models.CharField(max_length=500)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)

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

    unique_together = ('city', 'country')

    def __unicode__(self):
        return '%s, %s' % (self.city, self.country)


