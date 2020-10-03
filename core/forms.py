from django import forms
from .models import Customer
from .models import Contract

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'