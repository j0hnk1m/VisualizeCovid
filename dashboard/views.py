from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import scrape

def home_view(request, *args, **kwargs):
    latest = scrape.get_data()
    return render(request, 'home.html', latest)

def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

def sources_view(request, *args, **kwargs):
    return render(request, 'sources.html', {})

def news_view(request, *args, **kwargs):
    return render(request, 'news.html', {})
