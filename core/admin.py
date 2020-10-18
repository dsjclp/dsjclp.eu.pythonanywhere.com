from django.contrib import admin

from .models import Customer, Contract, Schedule, Step

admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Schedule)
admin.site.register(Step)