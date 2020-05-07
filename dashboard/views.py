from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import scrape
from django.utils import timezone


def home_view(request, *args, **kwargs):
    if scrape.get_countries().count() == 0 or (timezone.now()-scrape.get_global().last_updated).total_seconds()/3600 > 24:
        scrape.fetch_api_data()
        scrape.fetch_time_data2()

    return render(request, 'home.html', {
                                            'global': scrape.get_global(),
                                            'countries': scrape.get_countries(),
                                            'all_dates': scrape.get_dates()
                                        })


def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def news_view(request, *args, **kwargs):
    return render(request, 'news.html', {})
