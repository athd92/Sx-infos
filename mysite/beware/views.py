from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
import requests
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, FileResponse, HttpResponse
from .forms import UserCustomLoginForm, ContactForm, SearchForm
import time
import whois
import io
from reportlab.pdfgen import canvas
import random


def charts(request):
    if request.user.is_authenticated:
        user = request.user.username
        os = request.user_agent.os.family  # returns 'iOS'
        user_selected = User.objects.get(username=user)
        last_conn = user_selected.last_login
        context = {"last_conn": last_conn, "user": user, "os": os}
        return render(request, "beware/charts.html", context)
    else:
        return redirect("/")


def get_next_launch(request):
    # if request.method == "GET":
    #     client_ip = request.META.get("REMOTE_ADDR")
    #     resp = JsonResponse({"data": client_ip})
    #     return resp
    if request.method == "GET":
        resp = requests.get("https://api.spacexdata.com/v3/launches/next")
        resp = resp.json()
        mission_name = resp.get("mission_name")
        machine = resp.get("rocket").get("rocket_id")
        date = resp.get("launch_date_utc")
        date = date[0:10]
    context = {"mission_name": mission_name, "machine": machine, "date": date}
    resp = JsonResponse({"data": context})
    return resp


def get_random(request):
    x = random.randrange(4)
    resp = requests.get(f"https://api.spacexdata.com/v3/history/{x}")
    resp = resp.json()
    story_title = resp.get("title")
    details = resp.get("details")
    context = {"title": story_title, "details": details}
    resp = JsonResponse({"data": context})
    return resp


def getreferer(request):
    if request.method == "GET":
        referer = request.META.get("REMOTE_HTTP_REFERER")
        referer = JsonResponse({"referer": referer})
        return referer


def getdns(request):
    if request.method == "GET":
        client_ip = request.META.get("REMOTE_ADDR")
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
    form = SearchForm()
    context = {"form": form}
    return render(request, "beware/index.html", context)


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
    return render(request, "beware/register.html", {"form": form})


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
            request=request, template_name="beware/login.html", context={"form": form}
        )


def graph(request):
    return render(request, template_name="beware/charts.html")


def contact(request):
    form = ContactForm
    return render(request, "beware/contact.html", {"form": form,})


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
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


def search(request):
    form = SearchForm(request.POST)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                query = form.cleaned_data.get("search")
                print("")
                print(query)

                user = request.user.username
                os = request.user_agent.os.family  # returns 'iOS'
                user_selected = User.objects.get(username=user)
                last_conn = user_selected.last_login
                context = {"last_conn": last_conn, "user": user, "os": os}
                return render(request, "beware/charts.html", context)
    else:
        return redirect("/")
