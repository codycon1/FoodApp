"""GunniGrubRewrite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

import accounts.urls
import homepage.urls
import db.urls
import management.urls
import order.urls
import processorder.urls
import legal.urls
import currentorders.urls
import subscription.urls


# This is the MAIN URL router, all apps should be included here
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(accounts.urls)),
    path('', include(homepage.urls)),
    path('', include(db.urls)),
    path('', include(management.urls)),
    path('', include(order.urls)),
    path('', include(processorder.urls)),
    path('', include(legal.urls)),
    path('', include(currentorders.urls)),
    path('', include(subscription.urls)),
]
