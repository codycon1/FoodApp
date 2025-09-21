from django.db import models

# Create your models here.
from accounts.models import StandardUser


class Subscription(models.Model):
    user = models.ForeignKey(StandardUser, on_delete=models.CASCADE)
    time = models.IntegerField()
    submitDateTime = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


