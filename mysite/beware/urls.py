"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request, name="login_request"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout_request"),
    path('contact/', views.contact, name="contact"),
    path('charts/', views.charts, name="charts"),
    path('graph/', views.graph, name='graph'),
    path('get_next_launch/', views.get_next_launch, name="get_next_launch"),
    path('get_random/', views.get_random, name="get-random"),
    path('getdns/', views.getdns, name="getdns"),
    path('getreferer/', views.getreferer, name="getreferer"),
    path('results/', views.results, name='results'),
    path('search/', views.search, name='search'),
    path('picture/', views.picture, name='picture')
]
