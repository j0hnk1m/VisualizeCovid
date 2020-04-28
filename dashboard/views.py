from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import api


def home_view(request, *args, **kwargs):
    latest = api.fetch_api_data()
    print(latest)
    country_data = api.get_country_data()
    return render(request, 'home.html', {'latest': latest, 'country_data': country_data})

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def sources_view(request, *args, **kwargs):
    return render(request, 'sources.html', {})

def news_view(request, *args, **kwargs):
    return render(request, 'news.html', {})
