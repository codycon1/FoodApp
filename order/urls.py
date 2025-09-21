from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('order', views.startorder),
    path('order/list', views.listbyregion),
    path('order/id', views.orderbyID),
    path('order/stripe', views.StripeCheckout),
]
