from django.shortcuts import render
from django.views import generic
from .models import Customer
from .forms import CustomerForm
from .models import Contract
from .forms import ContractForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect



class CustomerListView(generic.ListView):
    model = Customer
    template_name = 'core/customer_list.html'

class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'core/customer_detail.html'

def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('/core/customers')
    else:
        form = CustomerForm()
    return render(request, 'core/customer_create.html', {'form': form})

    
class ContractListView(generic.ListView):
    model = Contract
    template_name = 'core/contract_list.html'

class ContractDetailView(generic.DetailView):
    model = Contract
    template_name = 'core/contract_detail.html'

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



from django.shortcuts import render

#pylint: disable=unused-argument

def dash_example_1_view(request, template_name="core/demo_six.html", **kwargs):
    'Example view that inserts content into the dash context passed to the dash application'

    context = {}

    # create some context to send over to Dash:
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['django_to_dash_context'] = "I am Dash receiving context from Django"
    request.session['django_plotly_dash'] = dash_context

    return render(request, template_name=template_name, context=context)

def session_state_view(request, template_name, **kwargs):

    session = request.session

    demo_count = session.get('django_plotly_dash', {})

    ind_use = demo_count.get('ind_use', 0)
    ind_use += 1
    demo_count['ind_use'] = ind_use
    session['django_plotly_dash'] = demo_count

    # Use some of the information during template rendering
    context = {'ind_use' : ind_use}

    return render(request, template_name=template_name, context=context)


def table_view(request, template_name="core/demo_six.html", **kwargs):
    'Example view that inserts content into the dash context passed to the dash application'

    customers = Customer.objects.all()
    toto = []
    for customer in customers:
        toto.append(customer.first_name)

    context = {}
    context['data'] = '{"dropdown-color": {"value": "green"}}'


    return render(request, template_name=template_name, context=context)