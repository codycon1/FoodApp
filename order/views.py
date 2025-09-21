import datetime
import decimal

import requests
import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from twilio.base.exceptions import TwilioRestException

from FoodApp import settings
from db.models import Restaurant, Stats

from twilio.rest import Client

from .forms import *


# Create your views here.


# BEGIN ORDER
# Select a restaurant

def getplaceID(user):
    searchquery = user.address + ' ' + str(user.zipcode)
    searchquery = searchquery.replace(' ', '+')
    searchqueryurl = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=' + settings.GOOGLE_API_KEY + '&input=' + searchquery + '&inputtype=textquery'
    searchresult = requests.get(searchqueryurl)
    searchdata = searchresult.json()
    try:
        placeID = searchdata['candidates'][0]['place_id']
    except IndexError:
        return None
    return placeID


def calculateDistance(sourcePlaceID, destPlaceID):
    # test query for distance
    distancequeryurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=' + settings.GOOGLE_API_KEY + '&origins=place_id:' + sourcePlaceID + '&destinations=place_id:' + destPlaceID
    response = requests.get(distancequeryurl)
    responsedata = response.json()

    mileage = (responsedata['rows'][0]['elements'][0]['distance']['text']).split(' ')
    mileage = int(float(mileage[0]))
    # THIS IS IN FUCKING KILOMETERS
    mileage = int(mileage / 1.609)
    return mileage


def calculateMileageCost(mi, region):
    if region.winterStatus:
        if region.deliveryRadiusWinter < mi:
            mileageCost = round(((mi - region.deliveryRadiusWinter) * region.deliveryRateWinter), 2)
            return mileageCost
        else:
            return 0
    else:
        if region.deliveryRadius < mi:
            mileageCost = round(((mi - region.deliveryRadius) * region.deliveryRate), 2)
            return mileageCost
        else:
            return 0

    return round(float(cost), 2)


def submitOrder(customerID, restaurantID, date, time, special, charge, mileagecharge, tip, chargetype):
    customerObject = StandardUser.objects.get(id=customerID)
    restaurantObject = Restaurant.objects.get(id=restaurantID)

    order_instance = Order.objects.create(name=(customerObject.first_name + ' ' + customerObject.last_name))
    order_instance.customerID = customerObject
    order_instance.restaurantID = restaurantObject
    order_instance.region = customerObject.region
    order_instance.phone = customerObject.phone
    order_instance.dateDelivery = date
    order_instance.timeDelivery = time
    order_instance.deliveryAddress = customerObject.address + " " + customerObject.address2
    order_instance.specialRequests = special
    order_instance.mileagecharge = mileagecharge
    order_instance.basecharge = charge
    order_instance.tip = tip
    total = mileagecharge + charge + tip
    order_instance.totalcharge = total

    if chargetype == 'cash':
        order_instance.chargetype = 'cash'
        order_instance.status = 'placed'
    elif chargetype == 'card':
        order_instance.chargetype = 'card'
        order_instance.status = 'pending'

    order_instance.save()
    UpdateStats(total - tip)
    if order_instance.status == 'placed':
        alertDrivers(restaurantObject.name, date, time)
    return order_instance.id


def alertDrivers(restaurantName, date, time):
    recips = StandardUser.objects.filter(driver=True)

    sid = settings.TWILIO_SITE_ID
    token = settings.TWILIO_AUTH_TOKEN
    client = Client(sid, token)
    for users in recips:
        if users.phone is not None:
            try:
                destination = users.phone.as_e164
                message = client.messages.create(
                    body="GUNNIGRUB: A new order has been received.\n" + 'Restaurant:\n' + str(
                        restaurantName) + '\nAt:\n' + str(date) + ' ' + str(time),
                    from_='+19706844782',
                    to=destination
                )
            except TwilioRestException as e:  # Twilio non-subscribed recipient handler (do nothing)
                pass


def alertCustomer(customer, stage):
    print("alerting customer" + customer.phone.as_e164)
    stageDict = {
        0: "Thank you for placing your GunniGrub order! You will receive periodic notifications regarding your order status.",
        1: "Your order has been accepted.",
        2: "Your order has been picked up.",
        3: "Your order has been delivered. Thank you!",
    }
    sid = settings.TWILIO_SITE_ID
    token = settings.TWILIO_AUTH_TOKEN
    client = Client(sid, token)
    print(customer.SMSOptIn)
    if customer.phone is not None and customer.SMSOptIn:
        try:
            destination = customer.phone.as_e164
            message = client.messages.create(
                body=stageDict[stage],
                from_='+19706844782',
                to=destination
            )

        except TwilioRestException as e:  # Twilio non-subscribed recipient handler (do nothing)
            pass


def checkHours(region):
    now = datetime.datetime.now()
    timenow = now.time()
    weekday = now.weekday()  # monday is 0 sunday is 6

    weekdayDict = {
        0: (region.onMonday, region.offMonday),
        1: (region.onTuesday, region.offTuesday),
        2: (region.onWednesday, region.offWednesday),
        3: (region.onThursday, region.offThursday),
        4: (region.onFriday, region.offFriday),
        5: (region.onSaturday, region.offSaturday),
        6: (region.onSunday, region.offSunday),
    }

    return weekdayDict[weekday][0] <= timenow <= weekdayDict[weekday][1]


@login_required
def startorder(request):
    user = request.user
    if '' in (user.region, user.address, user.zipcode, user.phone):
        messages.info(request, 'Please fill out your delivery information.')
        return redirect('/registration/profile/')

    if (checkHours(user.region)):
        return render(request, 'order/start.html', {'user': user, })
    else:
        messages.info(request, "We're sorry, we are currently closed. Please take a look at our hours of operation")
        return redirect('/hours')


@login_required
def listbyregion(request):
    region = request.user.region
    choices = Restaurant.objects.filter(region=region)

    return render(request, 'order/list.html', {'choices': choices})


@login_required
def orderbyID(request):
    restaurantID = request.GET.get('id')

    customerID = request.user.id

    restaurantObject = Restaurant.objects.get(id=restaurantID)

    sourcequery = restaurantObject.placeID

    destinationquery = getplaceID(request.user)
    if destinationquery is None:
        messages.info(request, 'Could not find address.')
        return redirect('/registration/profile/')

    mileage = calculateDistance(sourcequery, destinationquery)

    mileagecharge = calculateMileageCost(mileage, restaurantObject.region)

    if request.user.premiumValidDate >= datetime.date.today():
        basecharge = restaurantObject.region.baseChargeMember
    else:
        basecharge = restaurantObject.region.baseCharge
    total = mileagecharge + basecharge

    request.session['charge'] = float(total)

    if request.method == "POST":
        form = OrderDetails(request.POST)
        if form.is_valid():
            tip = request.POST.get('tip', default=float(0.00))
            if tip == "":
                tip = float(0.00)
            tip = decimal.Decimal(round(float(tip), 2))
            date = form.cleaned_data.get('dateDelivery')
            time = form.cleaned_data.get('timeDelivery')
            special = form.cleaned_data.get('specialRequests')
            if request.POST.get('charge') == 'cash':
                chargetype = 'cash'
                submitOrder(customerID, restaurantID, date, time, special, basecharge, mileagecharge, tip, chargetype)
                alertCustomer(request.user, 0)
                return redirect('/myorders')
            elif request.POST.get('charge') == 'card':
                chargetype = 'card'
                orderid = submitOrder(customerID, restaurantID, date, time, special, basecharge, mileagecharge, tip,
                                      chargetype)

                request.session['orderid'] = orderid
                request.session['basecharge'] = float(basecharge)
                request.session['mileagecharge'] = float(mileagecharge)
                request.session['tip'] = float(tip)

                return redirect('/order/stripe')

    else:
        form = OrderDetails

    context = {'choice': restaurantObject.name,
               'address': request.user.address,
               'fee': float(basecharge),
               'mileagecharge': float(mileagecharge),
               'total': float(total),
               'form': form}
    return render(request, 'order/orderbyid.html', context)


def UpdateStats(revenue):
    try:
        dailyStatsObject = Stats.objects.get(date=datetime.date.today())
    except Stats.DoesNotExist:
        dailyStatsObject = Stats.objects.create()

    dailyStatsObject.deliveryNumber += 1
    dailyStatsObject.dailyRevenue += revenue

    dailyStatsObject.save()


def StripeCheckout(request):
    stripe.api_key = settings.STRIPE_API_KEY
    session = stripe.checkout.Session.create(
        metadata={'orderid': request.session.get('orderid'), 'type': 'order'},
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(round(request.session.get('basecharge', 0), 2) * 100),
                    'product_data': {
                        'name': 'Delivery Fee',
                    },
                },
                'quantity': 1,
            },
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(round(request.session.get('mileagecharge', 0), 2) * 100),
                    'product_data': {
                        'name': 'Mileage',
                    },
                },
                'quantity': 1,
            },
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(round(request.session.get('tip', 0), 2) * 100),
                    'product_data': {
                        'name': 'Tip',
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=settings.UTIL_DOMAIN + '/myorders',
        cancel_url=settings.UTIL_DOMAIN + '/myorders',
    )
    return redirect(session.url, code=303)
