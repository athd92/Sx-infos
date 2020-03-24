from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
import requests
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, FileResponse, HttpResponse
from .forms import UserCustomLoginForm
import time
import whois
import io
from reportlab.pdfgen import canvas




def charts(request):
    if request.user.is_authenticated:
        user = request.user.username
        os = request.user_agent.os.family  # returns 'iOS'
        user_selected = User.objects.get(username=user)
        last_conn = user_selected.last_login
        print('')
        print('LAST')
        print(last_conn)
        context = {
            'last_conn': last_conn,
            'user': user,
            'os':os
        }
        return render(request, 'beware/charts.html', context)
    else:
        return redirect('/')

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

def register(request):

    if request.method == "POST":
        form = UserCustomLoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            login(request, user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                print("login failed")

            return render(
                request=request,
                template_name="beware/register.html",
                context={"form": form},
            )

    form = UserCustomLoginForm()
    return render(request, "beware/register.html", {'form':form})


def logout_request(request):
    """
    This function is used by the user to logout
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:
        return redirect("/")

def login_request(request):
    """
    This functions is used to get the user logged if
    the Auth is auth is success
    """
    if request.user.is_authenticated:
        return redirect("/")
    else:

        if request.method == "POST":
            print("PASSED ")
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    pass
            else:
                pass
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="beware/login.html",
            context={"form": form}
        )




def graph(request):
    return render(request, template_name="beware/charts.html")


def contact(request):
    return render(request, template_name="beware/contact.html")

def create_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')