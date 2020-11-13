from django.db import models
from django.contrib import admin
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    PARIS = 'Paris'
    MUNICH = 'Munich'
    BORDEAUX = 'Bordeaux'
    LORIENT = 'Lorient'
    CITY_CHOICES = [
        (PARIS, 'Paris'),
        (MUNICH, 'Munich'),
        (BORDEAUX, 'Bordeaux'),
        (LORIENT, 'Lorient'),
    ]
    city = models.CharField(max_length=99,
        choices=CITY_CHOICES,
        default=LORIENT,)

    def __str__(self):
        return '%s %s' % (self.id,self.city)
        
class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,)
    CREATED = 'Created'
    VALIDATED = 'Validated'
    ACTIVATED = 'Activated'
    CANCELLED = 'Cancelled'
    TERMINATED = 'Terminated'
    STATUS_CHOICES = [
        (CREATED, 'Created'),
        (VALIDATED, 'Validated'),
        (ACTIVATED, 'Activated'),
        (CANCELLED, 'Cancelled'),
        (TERMINATED, 'Terminated'),
    ]
    status = models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,)
    status_date = models.DateField(null=True, blank=True)

    creation_date = models.DateField(null=True, blank=True)
    validation_date = models.DateField(null=True, blank=True)
    activation_date = models.DateField(null=True, blank=True)
    cancellation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.id,self.status)

class Schedule(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.FloatField()
    rv = models.FloatField()
    rate = models.FloatField()
    ADVANCED = 'Advanced'
    ARREAR = 'Arrear'
    MODE_CHOICES = [
        (ADVANCED, 'Advanced'),
        (ARREAR, 'Arrear'),
    ]
    start_date = models.DateField(null=True, blank=True)
    mode = models.CharField(max_length=9,
        choices=MODE_CHOICES,
        default=ADVANCED,)

    def __str__(self):
        return str(self.id)

class Step(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    rent = models.FloatField()
    balance = models.FloatField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id)