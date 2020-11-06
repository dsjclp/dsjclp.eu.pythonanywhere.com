from django.shortcuts import render
from django.views import generic
from .models import Customer
from .forms import CustomerForm
from .models import Contract
from .forms import ContractForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Schedule
from .models import Step

class Dashboard(generic.TemplateView):
    template_name = "core/dashboard.html"

class Model(generic.TemplateView):
    template_name = "core/model.html"

def customers_list(request):
    customers=[]
    if request.user.is_authenticated:
        customers = Customer.objects.filter(user=request.user)
    return render(request, 'core/customers_list.html', {'customers': customers})

def contracts_list(request):
    contracts=[]
    if request.user.is_authenticated:
        contracts = Contract.objects.filter(user=request.user)
    return render(request, 'core/contracts_list.html', {'contracts': contracts})

def customer_detail(request,id):
    customer = get_object_or_404(Customer, pk=id)
    contracts = Contract.objects.filter(customer=customer)
    return render(request, 'core/customer_detail.html', {'customer': customer, 'contracts': contracts})

def contract_detail(request,id):
    contract = get_object_or_404(Contract, pk=id)
    schedules = Schedule.objects.filter(contract=contract)
    return render(request, 'core/contract_detail.html', {'contract': contract, 'schedules': schedules})

def schedule_detail(request,id):
    schedule = get_object_or_404(Schedule, pk=id)
    steps = Step.objects.filter(schedule=schedule)
    return render(request, 'core/schedule_detail.html', {'schedule': schedule, 'steps': steps})

def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('/core/customers')
    else:
        form = CustomerForm()
    return render(request, 'core/customer_create.html', {'form': form})

def contract_new(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.save()
            return redirect('/core/contracts')
    else:
        form = ContractForm()
    return render(request, 'core/contract_create.html', {'form': form})