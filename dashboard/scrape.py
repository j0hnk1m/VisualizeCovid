import requests
from .models import Country, Date
from datetime import datetime
from django.utils import timezone
from tqdm import tqdm
import pytz
import pickle
from collections import defaultdict


def update_country(name_, slug_, alpha2, alpha3, confirmed_, recovered_, deaths_, last_updated_):
    try:
        c = Country.objects.get(name=name_)
        if confirmed_ > c.confirmed:
            c.confirmed = confirmed_
            c.recovered = recovered_
            c.deaths = deaths_
            c.last_updated = last_updated_
            c.save(update_fields=['confirmed', 'recovered', 'deaths', 'last_updated'])
        return c
    except Country.DoesNotExist:
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


def update_date(date_, vals, c):
    date_ = datetime.strptime(date_, '%m/%d/%y').date()
    if not Date.objects.filter(country=c, date=date_).exists():
        Date.objects.create(
            date=date_,
            country=c,
            confirmed=vals[0],
            recovered=vals[1],
            deaths=vals[2]
        )
        return False
    return True


def get_global():
    try:
        return Country.objects.get(name='Global')
    except Country.DoesNotExist:
        return


def get_countries():               
    return Country.objects.all()


def get_dates():
    return Date.objects.all()


def get_last_updated():
    return


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
        timezone.make_aware(datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%SZ'))
    )

    # Countries stats
    for i in tqdm(data['Countries']):
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
            timezone.make_aware(datetime.strptime(i['Date'], '%Y-%m-%dT%H:%M:%SZ'))
        )
    
    print("*****************UPDATED DATABASE (COUNTRY)*****************")


def fetch_time_data():
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
                timezone.make_aware(datetime.strptime(data[-1]['Date'], '%Y-%m-%dT%H:%M:%SZ'))
            )
            for date in data[::-1]:
                update_date(date, c)
        
    print("*****************UPDATED DATABASE (TIME)*****************")


def fetch_time_data2():
    data = requests.get('https://covid19api.herokuapp.com').json()
    codes = load_codes()
    info = defaultdict(lambda: defaultdict(int))

    for category in tqdm(['confirmed', 'recovered', 'deaths']):
        locations = data[category]['locations']
        for h,i in enumerate(locations):
            alpha3 = '   '
            if i['country_code'] in codes:
                alpha3 = codes[i['country_code']]
            
            info[i['country']][category] += i['latest']
            info[i['country']]['alpha2_code'] = i['country_code']
            info[i['country']]['alpha3_code'] = alpha3
            info[i['country']]['last_updated'] = data['updatedAt']

            if 'history' not in info[i['country']]:
                info[i['country']]['history'] = defaultdict(lambda: [0, 0, 0])
            
            for k, v in i['history'].items():
                x = 0
                if category == 'recovered':
                    x = 1
                elif category == 'deaths':
                    x = 2
                info[i['country']]['history'][k][x] += v
    
    if 0 in info:
        del info[0]
    
    for country in tqdm(list(info.keys())):
        c = update_country(
            country, 
            country.lower(),
            info[country]['alpha2_code'],
            info[country]['alpha3_code'],
            info[country]['confirmed'],  
            info[country]['recovered'], 
            info[country]['deaths'],
            timezone.make_aware(datetime.strptime(info[country]['last_updated'][:-7], '%Y-%m-%d %H:%M:%S'))
        )

        history = info[country]['history']
        for date in list(history.keys())[::-1]:
            if update_date(date, history[date], c):  # if date already exists
                break
    
    print("*****************UPDATED DATABASE (TIME)*****************")
