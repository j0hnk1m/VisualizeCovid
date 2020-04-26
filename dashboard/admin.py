from django.contrib import admin

from .models import Country, Province, Case, Coordinate, Stat

# Register your models here.
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Case)
admin.site.register(Coordinate)
admin.site.register(Stat)
