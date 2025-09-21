from django.contrib import admin
from django.urls import path

from subscription import views

urlpatterns = [
    path('subscribe', views.subscribe),
    path('subscribebuy', views.subscribebuy),
    path('subscribestripe', views.StripeSubCheckout),
]
