import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from FoodApp import settings


def subscribe(request):
    return render(request, 'subscription/subscription.html')


@login_required
def subscribebuy(request):
    if request.GET.get('time'):
        stime = request.GET.get('time')
        if stime == "1mo":
            request.session['months'] = 1
            request.session['price'] = 10
        elif stime == "3mo":
            request.session['months'] = 3
            request.session['price'] = 25
        elif stime == "6mo":
            request.session['months'] = 6
            request.session['price'] = 40
        else:
            return redirect('/')

        return redirect('/subscribestripe')
    else:
        return redirect('/subscribe')


def StripeSubCheckout(request):
    stripe.api_key = settings.STRIPE_API_KEY
    months = request.session.get('months')
    price = request.session.get('price')
    session = stripe.checkout.Session.create(
        metadata={'user': request.user.email, 'months': months, 'type': 'subscription', 'price': price},
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(round(price, 2) * 100),
                    'product_data': {
                        'name': f'FoodApp Subscription: {months} months',
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=settings.UTIL_DOMAIN + '/subscribe',
        cancel_url=settings.UTIL_DOMAIN + '/subscribe',
    )
    return redirect(session.url, code=303)
