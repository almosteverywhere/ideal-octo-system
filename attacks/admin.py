from django.contrib import admin

# Register your models here.
from .models import Attack, Location

admin.site.register(Attack)
admin.site.register(Location)