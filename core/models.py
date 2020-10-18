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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    idcard = models.CharField(max_length=9)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20, default="Paris")

    def __str__(self):
        return '%s %s %s' % (self.id,self.first_name,self.last_name)
        

class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=100000)
    rv = models.PositiveIntegerField(default=0)
    creation_date = models.DateField(null=True, blank=True)
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DECLINED = 'Declined'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]
    status = models.CharField(max_length=9,
        choices=STATUS_CHOICES,
        default=PENDING,)
    status_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Schedule(models.Model):
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