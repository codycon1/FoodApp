import datetime

import stripe
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from FoodApp import settings
from order.views import alertDrivers, alertCustomer

stripe.api_key = settings.STRIPE_API_KEY

endpoint_secret = settings.STRIPE_WEBHOOK

from django.http import HttpResponse
from db.models import Order
from accounts.models import StandardUser
from subscription.models import Subscription


@csrf_exempt
def striperesponse(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Process the webhook response here
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session['metadata']['type'] == "order":
            print("New order")
            orderid = session['metadata']['orderid']
            orderObject = Order.objects.get(id=orderid)
            orderObject.status = 'placed'
            orderObject.save()
            alertDrivers(orderObject.restaurantID.name, orderObject.dateDelivery, orderObject.timeDelivery)
            alertCustomer(orderObject.customerID, 0)
        elif session['metadata']['type'] == "subscription":
            print("New subscription")
            userid = session['metadata']['user']
            months = session['metadata']['months']
            userobject = StandardUser.objects.get(email=userid)

            days = int(int(months) * 30)

            if userobject.premiumValidDate <= datetime.date.today():
                userobject.premiumValidDate = datetime.date.today() + datetime.timedelta(days=days)
                userobject.save()
            elif userobject.premiumValidDate > datetime.date.today():
                userobject.premiumValidDate += datetime.timedelta(days=days)
                userobject.save()

            subscriptioninstance = Subscription.objects.create(
                user=userobject,
                time=months,
                amount=session['metadata']['price']
            )
    # Passed signature verification
    return HttpResponse(status=200)
