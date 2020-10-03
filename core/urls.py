from django.urls import include, path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('accounts', include('django.contrib.auth.urls')),
    path('customers', views.CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/new/', views.customer_new, name='customer_new'),
    path('contracts', views.ContractListView.as_view(), name='contract_list'),
    path('contract/<int:pk>/', views.ContractDetailView.as_view(), name='contract_detail'),
    path('contract/new/', views.contract_new, name='contract_new'),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)