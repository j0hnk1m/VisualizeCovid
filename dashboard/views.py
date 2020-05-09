from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import scrape
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt


def home_view(request, *args, **kwargs):
    if scrape.get_countries().count() == 0 or (timezone.now()-scrape.get_global().last_updated).total_seconds()/3600 > 24:
        scrape.fetch_api_data()
        scrape.fetch_time_data2()

    return render(request, 'home.html', {
                                            'global': scrape.get_global(),
                                            'countries': scrape.get_countries()
                                        })
        
@csrf_exempt
def fetch_dates(request):
    if request.is_ajax and request.method == "GET":
        code = request.GET.get('code')
        try:
            data = scrape.get_dates()[code]
        except:
            data = {}
        print(data)
        return HttpResponse(json.dumps(data))


def about_view(request, *args, **kwargs):
    return render(request, 'about.html', {})
