import datetime

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from .databaseOptions import *
from accounts.models import StandardUser


# Main models for restaurants, orders, regions, and driver profiles are defined here
class Region(models.Model):
    # Basic info
    name = models.TextField(max_length=120, blank=False)
    code = models.CharField(max_length=3, blank=False)
    zip = models.IntegerField(null=False)

    active = models.BooleanField(default=True)

    # Charge info
    winterStatus = models.BooleanField(default=False)

    baseCharge = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRadius = models.DecimalField(max_digits=4, decimal_places=1)
    deliveryRate = models.DecimalField(max_digits=5, decimal_places=2)

    baseChargeWinter = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRadiusWinter = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRateWinter = models.DecimalField(max_digits=6, decimal_places=2)

    baseChargeMember = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRadiusMember = models.DecimalField(max_digits=4, decimal_places=1)
    deliveryRateMember = models.DecimalField(max_digits=5, decimal_places=2)

    baseChargeWinterMember = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRadiusWinterMember = models.DecimalField(max_digits=6, decimal_places=2)
    deliveryRateWinterMember = models.DecimalField(max_digits=6, decimal_places=2)

    # Hourly info - not ideal but it works for now - define operating hours for each day of the week
    onMonday = models.TimeField(verbose_name="Monday open time", default=datetime.time(8, 0, 0))
    offMonday = models.TimeField(verbose_name="Monday close time", default=datetime.time(8, 0, 0))
    onTuesday = models.TimeField(verbose_name="Tuesday open time", default=datetime.time(8, 0, 0))
    offTuesday = models.TimeField(verbose_name="Tuesday close time", default=datetime.time(8, 0, 0))
    onWednesday = models.TimeField(verbose_name="Wednesday open time", default=datetime.time(8, 0, 0))
    offWednesday = models.TimeField(verbose_name="Wednesday close time", default=datetime.time(8, 0, 0))
    onThursday = models.TimeField(verbose_name="Thursday open time", default=datetime.time(8, 0, 0))
    offThursday = models.TimeField(verbose_name="Thursday close time", default=datetime.time(8, 0, 0))
    onFriday = models.TimeField(verbose_name="Friday open time", default=datetime.time(8, 0, 0))
    offFriday = models.TimeField(verbose_name="Friday close time", default=datetime.time(8, 0, 0))
    onSaturday = models.TimeField(verbose_name="Saturday open time", default=datetime.time(8, 0, 0))
    offSaturday = models.TimeField(verbose_name="Saturday close time", default=datetime.time(8, 0, 0))
    onSunday = models.TimeField(verbose_name="Sunday open time", default=datetime.time(8, 0, 0))
    offSunday = models.TimeField(verbose_name="Sunday close time", default=datetime.time(8, 0, 0))

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    # basic info
    name = models.TextField(max_length=120, blank=False)
    website = models.URLField(blank=True)
    menu = models.URLField(blank=True)
    address = models.TextField(max_length=120, blank=False)
    phone = PhoneNumberField(null=True, blank=False)

    active = models.BooleanField(default=True)

    # region info
    region = models.ForeignKey(Region, related_name='RestaurantRegion', on_delete=models.CASCADE, blank=True, null=True)

    # google maps placeID
    placeID = models.TextField(max_length=32, blank=True)

    # active status
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customerID = models.ForeignKey(StandardUser, related_name='OrderCustomer', on_delete=models.CASCADE, blank=True,
                                   null=True)

    restaurantID = models.ForeignKey(Restaurant, related_name='OrderRestaurant', on_delete=models.CASCADE, blank=True,
                                     null=True)

    region = models.ForeignKey(Region, related_name='OrderRegion', on_delete=models.CASCADE, blank=True, null=True)

    # Copy a user profile object here
    phone = PhoneNumberField(null=True, blank=True)

    datePlaced = models.DateField(auto_now_add=True, blank=True, null=True)
    timePlaced = models.TimeField(auto_now_add=True, blank=True, null=True)
    dateDelivery = models.DateField(blank=True, null=True)
    timeDelivery = models.TimeField(blank=True, null=True)

    name = models.TextField(blank=True, null=True)
    deliveryAddress = models.TextField(blank=True, null=True)
    specialRequests = models.TextField(blank=True, null=True)

    status = models.TextField(blank=True, null=True)

    standardUser = StandardUser.objects.filter()
    driverOptions = StandardUser.objects.filter(driver=True)

    driverID = models.ForeignKey(StandardUser, related_name='driverAssignment', on_delete=models.CASCADE, blank=True,
                                 null=True, limit_choices_to={'driver': True})

    mileagecharge = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    basecharge = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    totalcharge = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    chargetype = models.TextField(blank=True, null=True, choices={('cash', 'cash'), ('card', 'card')})


class Stats(models.Model):
    date = models.DateField(auto_now=True)
    dailyRevenue = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    deliveryNumber = models.IntegerField(default=0)


class DriverProfile(models.Model):
    user = models.ForeignKey(StandardUser, on_delete=models.CASCADE, unique=True)

    balance = models.DecimalField(max_digits=6, decimal_places=2)
    dailyOrderNumber = models.IntegerField()
    onClock = models.DateTimeField()

    orderNumber = models.IntegerField()
    revenue = models.DecimalField(max_digits=6, decimal_places=2)
