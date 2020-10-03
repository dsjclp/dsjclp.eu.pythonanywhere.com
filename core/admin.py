from django.contrib import admin

from .models import Customer, Contract

admin.site.register(Customer)
admin.site.register(Contract)