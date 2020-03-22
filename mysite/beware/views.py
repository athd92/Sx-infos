from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import requests
import json
from django.http import JsonResponse


def graph(request):
    print(request.META)
    for k, v in request.META.items():
        print(k, v)


def getip(request):
    if request.method == "GET":
        client_ip = request.META.get('REMOTE_ADDR')
        resp = JsonResponse({"data": client_ip})
        return resp
    

def getos(request):
    if request.method == 'GET':

        # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
        request.user_agent.browser
        browser = request.user_agent.browser.family  # returns 'Mobile Safari'
        browser_version = request.user_agent.browser.version  # returns (5, 1)

        # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
        request.user_agent.os
        operating_system = request.user_agent.os.family  # returns 'iOS'
        # returns (5, 1)
        operating_system_version = request.user_agent.os.version

        request.user_agent.device  # returns Device(family='iPhone')
        device = request.user_agent.device.family  # returns 'iPhone'
        user_agent = JsonResponse({"browser": browser,
                                   "browser_version": browser_version,
                                   "operating_system": operating_system,
                                   "operating_system_version": operating_system_version,
                                   "device": device,
                                   })

        return user_agent


def getreferer(request):
    if request.method == 'GET':
        referer = request.META.get('REMOTE_HTTP_REFERER')
        referer = JsonResponse({'referer': referer})
        return referer


def getdns(request):
    if request.method == "GET":
        client_ip = request.META.get('REMOTE_ADDR')
        resp = requests.get(f"http://ip-api.com/json/{client_ip}")
        if resp.status_code != 200:
                resp = {
                "status": "success",
                "country": "France",
                "countryCode": "FR",
                "region": "IDF",
                "regionName": "Ile de France",
                "city": "Paris",
                "zip": "75001",
                "lat": 39.0438,
                "lon": -77.4874,
                "timezone": "Central European Time",
                "isp": "-",
                "org": "-",
                "as": "-",
                "query": "−",
                }
                resp = resp.json()        
                context = JsonResponse({"resp": resp})
                return context

        else:
                resp = resp.json()
                form = AuthenticationForm()        
                context = JsonResponse({"resp": resp})
        return context





def results(request):

    return render(request=request, template_name="beware/results.html")


def index(request):
    return render(request, template_name="beware/index.html")
