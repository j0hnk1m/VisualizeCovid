import requests
import re
from .models import Country, Province, Case, Coordinate, Stat
from datetime import datetime
from django.utils import timezone
import time


def get_country(name_, code_):
    c = None
    try:
        c = Country.objects.filter(name=name_)[0]
    except IndexError:
        c = Country.objects.create(name=name_, code=code_)
    return c


def get_province(name_, c, coor, dt):
    p = None
    try:
        p = Province.objects.filter(name=name_)[0]
    except IndexError:
        p = Province.objects.create(
            name=name_, 
            country=c,
            datetime=dt
        )
        
        Stat.objects.create(province=p)

        Coordinate.objects.create(
            latitude=coor['latitude'], 
            longitude=coor['longitude'],
            province=p
        )
    return p


def update_stats(p, category, latest):
    s = Stat.objects.filter(province=p)[0]
    if category == 'confirmed':
        s.confirmed = latest
    elif category == 'recovered':
        s.recovered = latest
    elif category == 'deaths':
        s.deaths = latest
    s.save(update_fields=[category, 'province'])


def update_history(p, category, history):
    for d, v in history.items():
        Case.objects.create(
            date=datetime.strptime(d, "%m/%d/%y").date(),
            value=v,
            category=(category.upper(), category),
            province=p,
        )


def get_data():
    countries = Country.objects.all()
    countries.delete()

    # Fetch API data
    data = requests.get('https://covid19api.herokuapp.com').json()
    latest = data['latest']

    # Store data in our database
    start=time.time()
    for category in ['confirmed', 'recovered', 'deaths']:
        locs = data[category]['locations']
        for loc in locs:
            # Get country if already it already exists in database, otherwise create it
            c = get_country(loc['country'], loc['country_code'])

            # Create province object and fill in model fields
            p = get_province(
                loc['province'], 
                c, 
                loc['coordinates'], 
                timezone.now()
            )

            # # Updates province history and last updated time
            update_stats(p, category, loc['latest'])
            # update_history(p, category, loc['history'])
            p.datetime = timezone.now()
            p.save(update_fields=['datetime'])
    
    end=time.time()
    print(end-start)
    return latest
