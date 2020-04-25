import requests
import re
from .models import Covid19

def get_data():
    latest = requests.get('https://covid19api.herokuapp.com/latest').json()
    confirmed = requests.get('https://covid19api.herokuapp.com/confirmed').json()
    recovered = requests.get('https://covid19api.herokuapp.com/recovered').json()
    deaths = requests.get('https://covid19api.herokuapp.com/deaths').json()


    for country in data:
        covid19 = Covid19()
        covid19.save()
    
    return latest

def update_data():
    data = Covid19.objects.all()
    data.delete()
