import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Models for users are defined here


class StandardUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class StandardUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = StandardUserManager()

    # user's delivery information
    region = models.ForeignKey('db.Region', on_delete=models.CASCADE, blank=True, null=True)

    address = models.TextField(max_length=120, blank=True, verbose_name='Address')
    address2 = models.TextField(max_length=120, blank=True, verbose_name='Apartment or Unit Number', default="")
    zipcode = models.IntegerField(blank=True, null=True, verbose_name='Zip Code')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Phone Number')

    # user's membership status
    premiumValidDate = models.DateField(default=datetime.datetime(1999, 1, 1))

    # employee info if applicable
    driver = models.BooleanField(default=False)
    manager = models.BooleanField(default=False)

    SMSOptIn = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
