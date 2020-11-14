from django import forms
from .models import Customer
from .models import Contract
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['city']

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['customer']