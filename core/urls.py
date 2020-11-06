from django.urls import include, path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Load demo plotly apps - this triggers their registration
import core.dash_dashboard

app_name = 'core'

urlpatterns = [
    path('accounts', include('django.contrib.auth.urls')),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('customers', views.customers_list, name='customers_list'),
    path('contracts', views.contracts_list, name='contracts_list'),
    path('customer/<int:id>/', views.customer_detail, name='customer_detail'),
    path('contract/<int:id>/', views.contract_detail, name='contract_detail'),
    path('schedule/<int:id>/', views.schedule_detail, name='schedule_detail'),
    path('customer/new/', views.customer_new, name='customer_new'),
    path('contract/new/', views.contract_new, name='contract_new'),
    path('model', views.Model.as_view(), name='model'),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)