from django.contrib import admin
import requests

from FoodApp import settings
from db import models


# Register models specific to order management and assignment in the admin interface

def updateplaceID(modeladmin, request, queryset):
    for obj in queryset:
        searchquery = obj.address + ' ' + str(obj.region.zip)
        searchquery = searchquery.replace(' ', '+')
        searchqueryurl = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=' + settings.GOOGLE_API_KEY + '&input=' + searchquery + '&inputtype=textquery'
        searchresult = requests.get(searchqueryurl)
        searchdata = searchresult.json()
        placeID = searchdata['candidates'][0]['place_id']
        obj.placeID = placeID
        obj.save()


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    actions = [updateplaceID]
    list_display = ['name', 'website', 'menu', 'address', 'phone', 'region', 'placeID', 'active']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'restaurantID', 'phone', 'datePlaced', 'timePlaced', 'dateDelivery', 'timeDelivery',
                    'deliveryAddress', 'specialRequests',
                    'status', 'driverID', 'basecharge', 'mileagecharge', 'tip', 'totalcharge', 'chargetype', ]
    pass


@admin.register(models.Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'dailyRevenue', 'deliveryNumber']
    pass


@admin.register(models.DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'dailyOrderNumber', 'onClock', 'orderNumber', 'revenue']
    pass

# class RestaurantAdminRegistration(admin.ModelAdmin):
#     fields = ['name', 'website', 'menu', 'address', 'phone', 'placeID', 'locale']
#     list_display = ['name', 'website', 'menu', 'address', 'phone', 'placeID', 'locale']
#
#
# class OrderAdminRegistration(admin.ModelAdmin):
#     fields = ['customerID', 'restaurantID', 'restaurantName','phone', 'deliveryaddress', 'sourceaddress', 'deliveryzipcode',
#               'deliverydate', 'deliverytime', 'chargetype','name', 'special', 'status', 'driverID']
#     list_display = ['customerID', 'restaurantID', 'restaurantName','phone', 'deliveryaddress', 'sourceaddress', 'deliveryzipcode',
#                     'deliverydate', 'deliverytime', 'chargetype','name', 'special', 'status', 'driverID']
#
#
# admin.site.register(models.Restaurant, RestaurantAdminRegistration)
# admin.site.register(models.Order, OrderAdminRegistration)
