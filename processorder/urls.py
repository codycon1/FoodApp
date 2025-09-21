from django.contrib import admin
from django.urls import path

from processorder import views

urlpatterns = [
    path('webhook', views.striperesponse),
]
