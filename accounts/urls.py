from django.contrib import admin
from django.urls import path, include

from accounts import views

# Path definitions for user account management and registration

urlpatterns = [
    path('registration/signup/', views.user_signup),
    path('registration/profile/', views.user_region),
    path('registration/contact/', views.user_contact),
    path('registration/address/', views.user_address),
    path('registration/optin/', views.user_optin),
    path('registration/', include('django.contrib.auth.urls')),
]
