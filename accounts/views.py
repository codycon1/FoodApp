from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import *
from django.conf import settings
from django.shortcuts import redirect


# Create views for user registration and profile management, in multiple steps

def user_signup(request):
    if request.method == 'POST':
        form = StandardUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = StandardUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def user_region(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileRegion(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/registration/contact')
    else:
        form = UserProfileRegion(instance=user)
    return render(request, 'registration/region.html', {'form': form})


@login_required
def user_contact(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileContact(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/registration/address')
    else:
        form = UserProfileContact(instance=user)
    return render(request, 'registration/contact.html', {'form': form})


@login_required
def user_address(request):
    user=request.user
    if request.method == 'POST':
        form = UserProfileAddress(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/registration/optin')
    else:
        form = UserProfileAddress(instance=user)
    return render(request, 'registration/address.html', {'form': form})


@login_required
def user_optin(request):
    #TODO: OPT IN
    user=request.user
    if request.method == 'POST':
        form = UserProfileOptIn(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            messages.info(request, "Your profile was successfully updated.")
            return redirect('/')
    else:
        form = UserProfileOptIn(instance=user)
    return render(request, 'registration/optin.html', {'form': form})

    # currentaddress = user.address
    # currentzip = user.zipcode
    # currentphone = user.phone
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         if form.cleaned_data.get('zipcode') not in settings.VALID_ZIP:
    #             return render(request, 'outofservice.html', context={'failedzip': form.cleaned_data.get('zipcode')})
    #         #
    #         form.save(commit=True)
    #         return redirect('/')
    # else:
    #     form = ProfileForm({'address': currentaddress, 'zipcode': currentzip, 'phone': currentphone})
    # return render(request, 'registration/region.html', {'form': form})
