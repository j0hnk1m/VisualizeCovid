import requests
from .models import Country, Date
from datetime import datetime
from django.utils import timezone
from tqdm import tqdm
import pytz


def update_country(name_, code_, confirmed_, recovered_, deaths_, date_):
    try:
        c = Country.objects.get(name=name_, code=code_)
        c.confirmed = confirmed_
        c.recovered = recovered_
        c.deaths = deaths_
        c.last_updated = date_
        c.save(update_fields=['confirmed', 'recovered', 'deaths', 'last_updated'])
        return c
    except:
        if confirmed_ == 0:
            confirmed_ = 1
        
        return Country.objects.create(
            name=name_, 
            code=code_,
            confirmed=confirmed_,
            recovered=recovered_,
            deaths=deaths_,
            mortality=deaths_/confirmed_*100,
            last_updated=timezone.now()
        )


def update_dates(data, c):
    for i in data:
        datetime_ = datetime.strptime(i['Date'], '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.utc)
        try:
            Date.objects.get(datetime=datetime_, country=c)
            return
        except:
            Date.objects.create(
                datetime=datetime_,
                country=c,
                confirmed=i['Confirmed'],
                recovered=i['Recovered'],
                deaths=i['Deaths']
            )


def get_country_data():
    return Country.objects.all()


def get_date_data():
    return Date.objects.all()


def fetch_api_data():
    data = requests.get('https://api.covid19api.com/summary').json()
    latest = data['Global']

    for i in data['Countries']:
        c = update_country(
            i['Country'], 
            i['CountryCode'], 
            i['TotalConfirmed'], 
            i['TotalRecovered'], 
            i['TotalDeaths'], 
            datetime.strptime(i['Date'], '%Y-%m-%dT%H:%M:%SZ').astimezone(pytz.utc)
        )

    return latest


def update_time_data():
    countries = requests.get('https://api.covid19api.com/countries').json()

    for country in tqdm(countries):    
        data = requests.get(f"https://api.covid19api.com/total/country/{country['Slug']}").json()
        if len(data) > 0:
            c = update_country(
                country['Country'], 
                country['ISO2'], 
                data[-1]['Confirmed'], 
                data[-1]['Recovered'], 
                data[-1]['Deaths']
            )
            update_dates(data[:-1], c)
