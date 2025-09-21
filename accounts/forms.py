from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import StandardUser

from db.models import Region

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

# Define forms for user profile management, registration is in multiple steps
class UserProfileRegion(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].required = True

    class Meta:
        model = StandardUser
        fields = ('region',)


class UserProfileContact(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone'].required = True

    class Meta:
        model = StandardUser
        fields = ('first_name', 'last_name', 'phone',)


class UserProfileAddress(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['zipcode'].required = True

    class Meta:
        model = StandardUser
        fields = ('address', 'address2', 'zipcode',)

# Gather consent for SMS notifications
class UserProfileOptIn(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = StandardUser
        fields = ('SMSOptIn',)


class StandardUserCreationForm(UserCreationForm):

    class Meta:
        model = StandardUser
        fields = ('email',)


# class StandardUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = StandardUser
#         fields = ('email',)
#
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = StandardUser
#         fields = ()
#
#     def save(self, commit=True):
#         user = super(ProfileForm, self).save(commit=False)
#         if commit:
#             user.save()
#         return user
#
#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=64, help_text='Required.')
#
#     class Meta:
#         model = StandardUser
#         fields = ('email', 'password1', 'password2')
