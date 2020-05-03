import requests
from .models import Country, Date
from datetime import datetime
from django.utils import timezone
from tqdm import tqdm
import pytz
import pickle


def update_country(name_, slug_, alpha2, alpha3, confirmed_, recovered_, deaths_, date_):
    try:
        c = Country.objects.get(name=name_, alpha2_code=alpha2)
        c.confirmed = confirmed_
        c.recovered = recovered_
        c.deaths = deaths_
        c.last_updated = date_
        c.save(update_fields=['confirmed', 'recovered', 'deaths', 'last_updated'])
        return c
    except:
        if confirmed_ == 0:
            mortality_ = 0
        else:
            mortality_ = deaths_ / confirmed_
        
        return Country.objects.create(
            name=name_, 
            slug=slug_,
            alpha2_code=alpha2,
            alpha3_code=alpha3,
            confirmed=confirmed_,
            recovered=recovered_,
            deaths=deaths_,
            mortality=mortality_*100,
            last_updated=datetime.now().date()
        )


def update_dates(data, c):
    for i in data:
        date_ = datetime.strptime(i['Date'], '%Y-%m-%dT%H:%M:%SZ').date()
        try:
            Date.objects.get(date=date_, country=c)
            return
        except:
            Date.objects.create(
                date=date_,
                country=c,
                confirmed=i['Confirmed'],
                recovered=i['Recovered'],
                deaths=i['Deaths']
            )


def get_global():
    try:
        return Country.objects.get(name='Global')
    except:
        return


def get_countries():               
    return Country.objects.all()


def get_dates():
    return Date.objects.all()


# def save_codes(country_name, alpha2_code):
#     f = open('static/iso_3166_country_codes.json')
#     codes = {}
#     info = json.load(f)
#     for i in info:
#         codes[i['alpha_2']] = i['alpha_3']
    
#     with open('static/codes.pkl', 'wb') as f:
#         pickle.dump(codes, f, pickle.HIGHEST_PROTOCOL)


def load_codes():
    with open('static/codes.pkl', 'rb') as f:
        return pickle.load(f)


def fetch_api_data():
    data = requests.get('https://api.covid19api.com/summary').json()
    codes = load_codes()

    # Global stats
    update_country(
        'Global', 
        'global',
        '..', 
        '...',
        data['Global']['TotalConfirmed'], 
        data['Global']['TotalRecovered'], 
        data['Global']['TotalDeaths'], 
        datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%SZ').date()
    )

    # Countries stats
    for i in data['Countries']:
        try:
            alpha3 = codes[i['CountryCode']]
        except:
            alpha3 = '   '
        
        update_country(
            i['Country'], 
            i['Slug'],
            i['CountryCode'],
            alpha3, 
            i['TotalConfirmed'], 
            i['TotalRecovered'], 
            i['TotalDeaths'], 
            datetime.strptime(i['Date'], '%Y-%m-%dT%H:%M:%SZ').date()
        )
    
    print("*****************UPDATED DATABASE (COUNTRY)*****************")


def update_time_data():
    countries = requests.get('https://api.covid19api.com/countries').json()
    codes = load_codes()

    for country in tqdm(countries):  
        data = requests.get(f"https://api.covid19api.com/total/country/{country['Slug']}").json()
        try:
            alpha3 = codes[country['ISO2']]
        except:
            alpha3 = '   '
        
        if len(data) > 0:
            c = update_country(
                country['Country'], 
                country['Slug'],
                country['ISO2'],
                alpha3, 
                data[-1]['Confirmed'], 
                data[-1]['Recovered'], 
                data[-1]['Deaths'],
                datetime.strptime(data[-1]['Date'], '%Y-%m-%dT%H:%M:%SZ').date()
            )
            update_dates(data[:-1], c)
        
    print("*****************UPDATED DATABASE (TIME)*****************")

