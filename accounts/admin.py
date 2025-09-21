import django.contrib.auth.admin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from .forms import StandardUserCreationForm, StandardUserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from .models import StandardUser


# Register your models here.
@admin.register(StandardUser)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    fieldsets = (
        (None, {'fields': (
        'first_name', 'last_name', 'email', 'password', 'is_active', 'driver', 'manager', 'address', 'address2', 'zipcode', 'phone',
        'region','premiumValidDate', 'SMSOptIn')}),
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'is_active', 'driver', 'manager',)}),
    )
    # exclude = ['username',]
    ordering = ('email',)
    list_display = ['email', 'first_name', 'last_name', 'driver', 'phone', 'zipcode', 'region', 'premiumValidDate']

# class StandardUserAdmin(UserAdmin):
#     add_form = StandardUserCreationForm
#     form = StandardUserChangeForm
#     model = StandardUser
#     list_display = ['email', 'username']
#
#
# admin.site.register(StandardUser, StandardUserAdmin)
