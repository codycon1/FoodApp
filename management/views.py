import datetime

from django.shortcuts import render
from db.models import Stats


# Create your views here.
def manage(request):
    # TODO: Generate a stats entry if it does not exist, also generate stats entry if an order is placed and deos not
    #  exist for the day

    try:
        dailyStatsObject = Stats.objects.get(date=datetime.date.today())
    except Stats.DoesNotExist:
        dailyStatsObject = Stats.objects.create()
    context = {'dailystats': dailyStatsObject}

    return render(request, 'management/manager.html', context)
