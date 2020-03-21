from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import requests
import json


def index(request):
    print(request.META)
    for k,v in request.META.items():
        print(k,v)

    # client_ip = request.META.get('REMOTE_ADDR')
    # resp = requests.get(f"http://ip-api.com/json/127.0.0.1")
    # if resp.status_code != 200:
    #     resp = {
    #         "status": "success",
    #         "country": "France",
    #         "countryCode": "FR",
    #         "region": "IDF",
    #         "regionName": "Ile de France",
    #         "city": "Paris",
    #         "zip": "75001",
    #         "lat": 39.0438,
    #         "lon": -77.4874,
    #         "timezone": "Central European Time",
    #         "isp": "-",
    #         "org": "-",
    #         "as": "-",
    #         "query": "−",
    #     }
    #     resp = resp.json()
    #     context = {"resp": resp}
    #     return render(
    #         request=request, template_name="beware/index.html", context=context
    #     )

    # else:
    #     resp = resp.json()
    #     form = AuthenticationForm()
    #     context = {"resp": resp}
    return render(request=request, template_name="beware/index.html")


def results(request):

    return render(request=request, template_name="beware/results.html")

