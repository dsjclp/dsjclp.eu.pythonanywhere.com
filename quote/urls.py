from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url


from django.views.generic import TemplateView

# Load demo plotly apps - this triggers their registration
import quote.dash_quote, quote.dash_reverse, quote.dash_pr

# pylint: disable=unused-import

from django_plotly_dash.views import add_to_session

from django.conf import settings
from django.conf.urls.static import static


app_name = 'quote'

urlpatterns = [
    path('direct', views.QuotePage.as_view(), name='create_quote'),
    path('reverse', views.ReversePage.as_view(), name='create_reverse'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)