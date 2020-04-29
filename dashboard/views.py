from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import api


def home_view(request, *args, **kwargs):
    if get_countries().count == 0:
        api.fetch_api_data()
    
    glob = api.get_global()
    countries = api.get_countries()
    return render(request, 'home.html', {'global': glob, 'countries': countries})

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def sources_view(request, *args, **kwargs):
    return render(request, 'sources.html', {})

def news_view(request, *args, **kwargs):
    return render(request, 'news.html', {})
