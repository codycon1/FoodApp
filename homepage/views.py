from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import StandardUser
from db.models import Region, Restaurant


# Create your views here.
def home(request):
    return render(request, 'homepage/home.html')


def hours(request):
    user = request.user
    if user.region is None:
        messages.info(request, 'Please select your region.')
        return redirect('/registration/profile/')
    else:
        region = user.region

    context = {'monop': region.onMonday, 'moncl': region.offMonday,
               'tueop': region.onTuesday, 'tuecl': region.offTuesday,
               'wedop': region.onWednesday, 'wedcl': region.offWednesday,
               'thuop': region.onThursday, 'thucl': region.offThursday,
               'friop': region.onFriday, 'fricl': region.offFriday,
               'satop': region.onSaturday, 'satcl': region.offSaturday,
               'sunop': region.offSunday, 'suncl': region.offSunday}
    return render(request, 'homepage/hours.html', context)


def restaurantlist(request):
    context = {'restaurants': Restaurant.objects.select_related().order_by('region'), }

    return render(request, 'homepage/restaurants.html', context)
