from django.contrib import admin
from django.urls import path
import management.views
urlpatterns = [
    path('manager', management.views.manage)
]
