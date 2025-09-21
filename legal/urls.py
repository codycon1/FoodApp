from django.contrib import admin
from django.urls import path

from legal import views

urlpatterns = [
    path('privacy', views.privacypolicy),
    path('tos', views.termsofservice)
]
