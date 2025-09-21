from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import StandardUser
from db.models import Order

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class OrderDetails(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dateDelivery'].required = True
        self.fields['timeDelivery'].required = True
        self.fields['specialRequests'].required = False

    class Meta:
        model = Order
        fields = ('dateDelivery', 'timeDelivery', 'specialRequests')
        labels = {'dateDelivery': 'Pickup Date', 'timeDelivery': 'Pickup Time', 'specialRequests': 'Special Requests'}
        widgets = {
            'dateDelivery': DateInput(),
            'timeDelivery': TimeInput(),
        }
