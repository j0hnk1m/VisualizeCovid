import requests
import re
from .models import Country, Province
from datetime import datetime

def update_data():
    countries = Country.objects.all()
    countries.delete()

    data = requests.get('https://covid19api.herokuapp.com').json()
    latest = data['latest']

    for category in ['confirmed', 'recovered', 'deaths']:
        loc = data[category]['locations']

        # Get country if already it already exists in database, otherwise create it
        c = None
        try:
            c = Country.objects.filter(name=loc['country'])[0]
        except IndexError:
            c = Country.objects.create(name=loc['country'], code=loc['country_code'])

        # Create province object and fill in model fields
        p = None
        try:
            p = Province.objects.filter(name=loc['province'])[0]
        except:
            p = Province.objects.create(
                name=loc['province'], 
                country=c,
                latitude=loc['coordinates']['latitude'],
                longitude=loc['coordinates']['latitude'],
                datetime=datetime.now()
            )
        
        if category == 'confirmed':
            p.confirmed = loc['latest']
            p.confirmed_history = loc['history']
        elif category == 'recovered':
            p.recovered = loc['latest']
            p.recovered_history = loc['history']
        elif category == 'deaths':
            p.deaths = loc['latest']
            p.deaths_history = loc['history']
        p.datetime = datetime.now()
        p.save(update_fields=[category, f"{category}_history", 'datetime'])
        
    
    return latest

