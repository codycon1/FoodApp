from django.contrib import admin
from django.urls import path

from currentorders import views

# Link URL paths to views for current orders and driver interface if user is a driver

urlpatterns = [
    path('myorders', views.myorders),
    path('driver', views.driver)
]
