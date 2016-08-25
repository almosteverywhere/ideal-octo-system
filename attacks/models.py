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
