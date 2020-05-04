from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import scrape


def home_view(request, *args, **kwargs):
    if scrape.get_countries().count() == 0 or scrape.get_dates().count() == 0:
        scrape.fetch_api_data()
        scrape.fetch_time_data2()

    glob = scrape.get_global()
    countries = scrape.get_countries()
    return render(request, 'home.html', {'global': glob, 'countries': countries})

def update_db():
    return

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def news_view(request, *args, **kwargs):
    return render(request, 'news.html', {})
