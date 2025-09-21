from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from db.models import Order
from order.views import alertCustomer

#create views for current orders and driver interface

@login_required
def myorders(request):
    user = request.user
    context = {'orders': Order.objects.filter(customerID=user)}
    return render(request, 'currentorders/myorders.html', context)


@login_required
def driver(request):
    if not request.user.driver:
        return redirect('/')

    context = {}

    # Handle order status updates and detail view requests, this is not optimal but it works for now. 
    if request.method == 'POST':
        if request.POST.get('Assign Order', False):
            orderID = request.POST['id']
            query = Order.objects.get(id=orderID)
            query.status = "Accepted"
            query.driverID = request.user
            query.save()
            alertCustomer(query.customerID, 1)
        if request.POST.get('Picked up', False):
            orderID = request.POST['id']
            query = Order.objects.get(id=orderID)
            query.status = "Picked up"
            query.save()
            alertCustomer(query.customerID, 2)
        if request.POST.get('Complete', False):
            orderID = request.POST['id']
            query = Order.objects.get(id=orderID)
            query.status = "Complete"
            query.save()
            alertCustomer(query.customerID, 3)

    # Query the database for orders, only add context if an order ID is specified
    if request.method == 'GET' and 'id' in request.GET:
        orderID = request.GET.get('id')
        if orderID:
            context['detailview'] = Order.objects.get(id=orderID)

    context['dataset'] = Order.objects.filter(status="placed").order_by('dateDelivery', 'timeDelivery')
    context['myorders'] = Order.objects.filter(driverID=request.user)
    return render(request, 'management/driver.html', context)
